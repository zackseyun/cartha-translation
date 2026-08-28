#!/usr/bin/env python3
from __future__ import annotations
import argparse, concurrent.futures, copy, hashlib, json, os, pathlib, re, subprocess, sys, threading, time, urllib.error, urllib.request
from datetime import datetime, timezone
from typing import Any
import yaml

ROOT=pathlib.Path(__file__).resolve().parent.parent
TRANSLATION=ROOT/'translation'/'ot'
BOOKS=['psalms','job','proverbs','ecclesiastes','song_of_songs']
BOOK_CODES={'psalms':'PSA','job':'JOB','proverbs':'PRO','ecclesiastes':'ECC','song_of_songs':'SOL'}
API_VERSION=os.getenv('AZURE_OPENAI_API_VERSION','2025-04-01-preview')
SOL=os.getenv('WISDOM_AUDIT_SOL_DEPLOYMENT','gpt-5-6-sol-atlas')
TERRA=os.getenv('WISDOM_AUDIT_TERRA_DEPLOYMENT','gpt-5-6-terra-atlas')
LOCK=threading.Lock()

SOL_SYSTEM='''You are the primary source editor for the People's Open Bible Wisdom books. Review EVERY target verse against the supplied Westminster Leningrad Codex Hebrew, its immediate literary context, and the project's source-near editorial rules.

Authority order: Hebrew source and syntax; discourse and poetic structure; documented lexical evidence; natural modern English; comparison translations only as diagnostics.

Reject these failure modes: lexically possible but misleading gloss-English; dictionary fragments instead of natural English; unnecessary technical or archaic vocabulary; invented verbs, motives, adjectives, agents, doctrines, or resolved ambiguities; false species or object precision; and flattening a concrete image into its inferred effect. Translate ordinary Hebrew idioms into ordinary English and preserve meaningful literal forms or alternatives in notes. Preserve genuine ambiguity. Do not change a defensible verse merely to imitate familiar English. Treat explicit reader-triggered revisions from 2026-08-28 as controlling unless the Hebrew clearly disproves them.

Review every target ID. Default to unchanged. If revising, make the smallest complete correction. Inline footnote markers must exactly match the returned replacement footnotes when footnotes_mode=replace. If wording tied to a lexical decision changes, return matching lexical_updates so the audit trail cannot become stale. Never claim human or credentialed-scholar review.'''

TERRA_SYSTEM='''You are the independent adjudicator for a source-near English Bible audit. Evaluate each proposed change against the Hebrew, context, current text, documented reasoning, and editorial rules. Published English versions are diagnostics, not votes.

Approve only changes that correct meaning, unmarked interpretation, false precision, material register mismatch, or genuinely unnatural gloss-English. Reject mere preferences and regressions. You may revise a proposal to the smallest source-faithful natural-English correction. Preserve ambiguity and source images. Ensure footnote markers and lexical updates remain honest. Return a decision for every proposal. Never claim human or credentialed-scholar review.'''

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

def azure_env()->tuple[str,str]:
    ep=os.getenv('AZURE_OPENAI_ENDPOINT','').strip().rstrip('/'); key=os.getenv('AZURE_OPENAI_API_KEY','').strip()
    if ep and key:return ep,key
    acct=os.getenv('AZURE_OPENAI_ACCOUNT','cartha-aoai-truth-1c9177c8'); rg=os.getenv('AZURE_OPENAI_RESOURCE_GROUP','rg-cartha-truth-openai')
    key=subprocess.check_output(['az','cognitiveservices','account','keys','list','-g',rg,'-n',acct,'--query','key1','-o','tsv'],text=True).strip()
    ep=subprocess.check_output(['az','cognitiveservices','account','show','-g',rg,'-n',acct,'--query','properties.endpoint','-o','tsv'],text=True).strip().rstrip('/')
    return ep,key

def tool_schema(name:str, adjudication:bool=False)->dict[str,Any]:
    verdicts=['approve','reject','revise'] if adjudication else ['unchanged','revise']
    item={
      'type':'object','additionalProperties':False,
      'required':['id','verdict','revised_text','category','confidence','rationale','footnotes_mode','footnotes','lexical_updates'],
      'properties':{
        'id':{'type':'string'}, 'verdict':{'type':'string','enum':verdicts}, 'revised_text':{'type':'string'},
        'category':{'type':'string','enum':['unchanged','mistranslation','grammar','lexical','ambiguity','idiom','register','awkward_english','footnotes','other']},
        'confidence':{'type':'number','minimum':0,'maximum':1}, 'rationale':{'type':'string'},
        'footnotes_mode':{'type':'string','enum':['keep','replace']},
        'footnotes':{'type':'array','items':{'type':'object','additionalProperties':False,'required':['marker','text','reason'],'properties':{'marker':{'type':'string'},'text':{'type':'string'},'reason':{'type':'string'}}}},
        'lexical_updates':{'type':'array','items':{'type':'object','additionalProperties':False,'required':['source_word','chosen','rationale'],'properties':{'source_word':{'type':'string'},'chosen':{'type':'string'},'rationale':{'type':'string'}}}}
      }}
    return {'type':'function','function':{'name':name,'description':'Submit complete verse-by-verse source review results.','parameters':{'type':'object','additionalProperties':False,'required':['results'],'properties':{'results':{'type':'array','items':item}}}}}

def call_tool(endpoint:str,key:str,deployment:str,system:str,user:str,tool_name:str,retries:int=5)->tuple[dict[str,Any],dict[str,Any],str]:
    url=f'{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={API_VERSION}'
    tool=tool_schema(tool_name,adjudication=tool_name=='submit_adjudication')
    payload={'messages':[{'role':'system','content':system},{'role':'user','content':user}], 'max_completion_tokens':16000,'parallel_tool_calls':False,'tool_choice':{'type':'function','function':{'name':tool_name}},'tools':[tool]}
    raw=json.dumps(payload,ensure_ascii=False).encode()
    last=''
    for attempt in range(retries):
      try:
        req=urllib.request.Request(url,data=raw,headers={'Content-Type':'application/json','api-key':key},method='POST')
        with urllib.request.urlopen(req,timeout=360) as resp: body=json.loads(resp.read())
        msg=body['choices'][0]['message']; calls=msg.get('tool_calls') or []
        if len(calls)!=1: raise RuntimeError(f'expected one tool call, got {len(calls)}')
        fn=calls[0]['function'];
        if fn.get('name')!=tool_name: raise RuntimeError(f'wrong tool {fn.get("name")}')
        return json.loads(fn['arguments']),body.get('usage') or {},str(body.get('model') or deployment)
      except urllib.error.HTTPError as e:
        detail=e.read().decode(errors='replace'); last=f'HTTP {e.code}: {detail[:500]}'
        if e.code not in (429,500,502,503,504): raise RuntimeError(last)
        delay=float(e.headers.get('Retry-After') or min(60,5*(attempt+1)))
      except Exception as e:
        last=str(e); delay=min(30,3*(attempt+1))
      if attempt+1<retries: time.sleep(delay)
    raise RuntimeError(last)

def load_records(book:str,chapter:int|None=None)->list[tuple[pathlib.Path,dict[str,Any]]]:
  out=[]
  base=TRANSLATION/book
  for p in sorted(base.glob('*/*.yaml')):
    if chapter is not None and int(p.parent.name)!=chapter: continue
    d=yaml.safe_load(p.read_text()) or {}
    if isinstance(d,dict) and (d.get('translation') or {}).get('text'): out.append((p,d))
  return out

def compact_record(d:dict[str,Any])->dict[str,Any]:
  lex=[]
  for x in d.get('lexical_decisions') or []:
    lex.append({'source_word':str(x.get('source_word','')),'chosen':str(x.get('chosen','')),'alternatives':x.get('alternatives') or [],'rationale':str(x.get('rationale',''))[:500]})
  rev=(d.get('revisions') or [])[-2:]
  return {'id':d.get('id'),'reference':d.get('reference'),'source':d.get('source'),'current_text':(d.get('translation') or {}).get('text'),'footnotes':(d.get('translation') or {}).get('footnotes') or [],'lexical_decisions':lex,'theological_decisions':d.get('theological_decisions') or [],'recent_revisions':rev}

def chunks_for(book:str,records:list[tuple[pathlib.Path,dict[str,Any]]],size:int)->list[dict[str,Any]]:
  by_ch={}
  for p,d in records: by_ch.setdefault(int(p.parent.name),[]).append((p,d))
  chunks=[]
  for ch,rows in sorted(by_ch.items()):
    for start in range(0,len(rows),size):
      target=rows[start:start+size]; lo=max(0,start-2); hi=min(len(rows),start+size+2)
      context=[{'reference':x[1].get('reference'),'source_text':(x[1].get('source') or {}).get('text'),'current_text':(x[1].get('translation') or {}).get('text')} for x in rows[lo:hi]]
      chunks.append({'key':f'{book}-{ch:03d}-{start:03d}','book':book,'chapter':ch,'targets':[compact_record(d) for _,d in target],'context':context})
  return chunks

def validate_results(chunk:dict[str,Any],args:dict[str,Any],allowed:set[str])->list[dict[str,Any]]:
  results=args.get('results') or []; ids=[str(x.get('id')) for x in results]; expected=[str(x.get('id')) for x in chunk['targets'] if str(x.get('id')) in allowed]
  if sorted(ids)!=sorted(expected): raise RuntimeError(f"result IDs mismatch expected={expected} got={ids}")
  return results

def review_chunk(chunk:dict[str,Any],endpoint:str,key:str,checkpoint:pathlib.Path)->dict[str,Any]:
  out=checkpoint/f"{chunk['key']}.json"
  if out.exists(): return json.loads(out.read_text())
  prompt='# Complete source review\n\n'+json.dumps({'book':chunk['book'],'chapter':chunk['chapter'],'literary_context':chunk['context'],'target_records':chunk['targets']},ensure_ascii=False,indent=2)
  sol_args,sol_usage,sol_model=call_tool(endpoint,key,SOL,SOL_SYSTEM,prompt,'submit_chunk_review')
  sol_results=validate_results(chunk,sol_args,{str(x['id']) for x in chunk['targets']})
  proposals=[x for x in sol_results if x.get('verdict')=='revise' and x.get('revised_text')]
  adjud=[]; terra_usage={}; terra_model=TERRA
  if proposals:
    originals={str(x['id']):x for x in chunk['targets']}
    tp='# Independent adjudication\n\n'+json.dumps({'book':chunk['book'],'chapter':chunk['chapter'],'proposals':[{'original':originals[str(p['id'])],'proposal':p} for p in proposals]},ensure_ascii=False,indent=2)
    terra_args,terra_usage,terra_model=call_tool(endpoint,key,TERRA,TERRA_SYSTEM,tp,'submit_adjudication')
    adjud=validate_results(chunk,terra_args,{str(x['id']) for x in proposals})
  payload={'schema_version':1,'chunk':chunk['key'],'book':chunk['book'],'chapter':chunk['chapter'],'reviewed_at':now(),'sol_model':sol_model,'terra_model':terra_model,'sol_usage':sol_usage,'terra_usage':terra_usage,'sol_results':sol_results,'adjudications':adjud}
  tmp=out.with_suffix('.tmp'); tmp.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n'); tmp.replace(out)
  return payload

def marker_letters(text:str)->list[str]: return re.findall(r'\[([a-z])\]',text or '')

def approved_change(payload:dict[str,Any],rid:str)->dict[str,Any]|None:
  sol=next((x for x in payload['sol_results'] if str(x.get('id'))==rid),None)
  if not sol or sol.get('verdict')!='revise': return None
  adj=next((x for x in payload.get('adjudications',[]) if str(x.get('id'))==rid),None)
  if not adj or adj.get('verdict')=='reject' or float(adj.get('confidence') or 0)<0.88:return None
  return adj if adj.get('verdict') in ('approve','revise') else None

def apply_manifest(manifest:pathlib.Path)->dict[str,int]:
  stats={'reviewed':0,'revised':0,'unchanged':0,'escalated':0,'errors':0}
  path_index={}
  for book in BOOKS:
    for p in (TRANSLATION/book).glob('*/*.yaml'):
      m=re.search(r'^id:\s*[\"\']?([^\s\"\']+)',p.read_text(),re.M)
      if m: path_index[m.group(1)]=p
  for f in sorted(manifest.glob('*.json')):
    payload=json.loads(f.read_text()); book=payload['book']
    for sol in payload['sol_results']:
      rid=str(sol['id']); p=path_index.get(rid)
      if p is None: stats['errors']+=1; continue
      d=yaml.safe_load(p.read_text()) or {}; current=str((d.get('translation') or {}).get('text') or '')
      if (d.get('source_audit') or {}).get('reviewed_at')==payload.get('reviewed_at') and (d.get('source_audit') or {}).get('status')!='escalated':
        stats['reviewed']+=1; continue
      change=approved_change(payload,rid); audit_status='unchanged'
      adj=next((x for x in payload.get('adjudications',[]) if str(x.get('id'))==rid),None)
      if sol.get('verdict')=='revise' and adj and adj.get('verdict')=='reject':
        change=None; audit_status='unchanged'
      elif sol.get('verdict')=='revise' and change is None: audit_status='escalated'; stats['escalated']+=1
      elif change:
        new=str(change.get('revised_text') or '').strip(); mode=change.get('footnotes_mode')
        foot=change.get('footnotes') or []
        lex_updates=change.get('lexical_updates') or []
        if not all(isinstance(x,dict) for x in foot) or not all(isinstance(x,dict) for x in lex_updates):
          change=None; audit_status='escalated'; stats['escalated']+=1
        elif not new or new==current: change=None; audit_status='unchanged'
        elif mode=='replace' and sorted(marker_letters(new))!=sorted(str(x.get('marker')) for x in foot):
          change=None; audit_status='escalated'; stats['escalated']+=1
        elif mode=='keep' and sorted(marker_letters(new))!=sorted(str(x.get('marker')) for x in ((d.get('translation') or {}).get('footnotes') or [])):
          change=None; audit_status='escalated'; stats['escalated']+=1
        elif change.get('category')=='lexical' and not change.get('lexical_updates') and re.sub(r'\[[a-z]\]','',new)!=re.sub(r'\[[a-z]\]','',current):
          change=None; audit_status='escalated'; stats['escalated']+=1
        else:
          d['translation']['text']=new
          if mode=='replace': d['translation']['footnotes']=foot
          lexmap={str(x.get('source_word')):x for x in d.get('lexical_decisions') or []}
          valid=True
          for u in lex_updates:
            x=lexmap.get(str(u.get('source_word')))
            if not x:
              x={'source_word':str(u.get('source_word')),'chosen':u['chosen'],'alternatives':[],'lexicon':'HALOT/BDB source audit','rationale':u['rationale']}
              d.setdefault('lexical_decisions',[]).append(x); lexmap[str(u.get('source_word'))]=x
            else:
              x['chosen']=u['chosen']; x['rationale']=u['rationale']
          if not valid:
            d=yaml.safe_load(p.read_text()) or {}; change=None; audit_status='escalated'; stats['escalated']+=1
          else:
            audit_status='revised'; stats['revised']+=1
            d.setdefault('revisions',[]).append({'timestamp':payload['reviewed_at'],'adjudicator':'wisdom-source-audit','reviewer_model':f"{payload['sol_model']} + {payload['terra_model']}",'source_review':'WLC Hebrew, chapter context, documented POB reasoning, and public-domain comparison diagnostics','category':change.get('category'),'tier':1,'from':current,'to':new,'rationale':change.get('rationale')})
      if audit_status=='unchanged': stats['unchanged']+=1
      d['source_audit']={'status':audit_status,'reviewed_at':payload['reviewed_at'],'primary_model':payload['sol_model'],'adjudicator_model':payload['terra_model'] if sol.get('verdict')=='revise' else None,'scope':'WLC Hebrew, immediate literary context, natural-English and interpretation-boundary review','human_or_scholar_review':False,'review_summary':(change or sol).get('rationale','')[:1000]}
      p.write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False,width=10000),encoding='utf-8')
      stats['reviewed']+=1
  return stats

def main():
  ap=argparse.ArgumentParser(); ap.add_argument('--books',nargs='+',default=BOOKS); ap.add_argument('--chapter',type=int); ap.add_argument('--chunk-size',type=int,default=10); ap.add_argument('--concurrency',type=int,default=24); ap.add_argument('--checkpoint',type=pathlib.Path,required=True); ap.add_argument('--ids',nargs='*',default=[]); ap.add_argument('--apply',action='store_true'); ap.add_argument('--limit-chunks',type=int,default=0)
  a=ap.parse_args(); a.checkpoint.mkdir(parents=True,exist_ok=True)
  if a.apply:
    print(json.dumps(apply_manifest(a.checkpoint),indent=2)); return
  ep,key=azure_env(); chunks=[]
  for b in a.books:
    records=load_records(b,a.chapter)
    if a.ids: records=[row for row in records if str(row[1].get('id')) in set(a.ids)]
    chunks+=chunks_for(b,records,a.chunk_size)
  if a.limit_chunks:chunks=chunks[:a.limit_chunks]
  done=0; aggregate={'chunks':len(chunks),'proposals':0,'approved':0,'rejected':0,'errors':0}
  print(f"reviewing chunks={len(chunks)} books={a.books} sol={SOL} terra={TERRA} workers={a.concurrency}",flush=True)
  def worker(c): return review_chunk(c,ep,key,a.checkpoint)
  with concurrent.futures.ThreadPoolExecutor(max_workers=a.concurrency) as pool:
    futs={pool.submit(worker,c):c for c in chunks}
    for fut in concurrent.futures.as_completed(futs):
      done+=1
      try:
        r=fut.result(); props=sum(x.get('verdict')=='revise' for x in r['sol_results']); aggregate['proposals']+=props; aggregate['approved']+=sum(x.get('verdict') in ('approve','revise') for x in r.get('adjudications',[])); aggregate['rejected']+=sum(x.get('verdict')=='reject' for x in r.get('adjudications',[]))
      except Exception as e: aggregate['errors']+=1; print(f"ERROR {futs[fut]['key']}: {e}",flush=True)
      if done%10==0 or done==len(chunks): print(f"[{done}/{len(chunks)}] {aggregate}",flush=True)
  print(json.dumps(aggregate,indent=2))
if __name__=='__main__':main()
