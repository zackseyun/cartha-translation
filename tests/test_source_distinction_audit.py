import copy
import importlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

import yaml

os.environ.setdefault('CARTHA_DRAFTER_BACKEND', 'openai-sdk')
from tools import source_distinction_audit as audit
from tools import draft, gemini_review_worker as reviewer, azure_bulk_revise as azure
from tools import gemini_bulk_revise as gemini, auto_apply_gemini as auto, agentic_revise as agentic
from tools import simplified_pob_pipeline as spob

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = json.loads((ROOT / 'tests/fixtures/source_distinctions_john21_original.json').read_text())


def approved(n=15):
    return yaml.safe_load((ROOT / f'translation/nt/john/021/{n:03}.yaml').read_text())


def checks(record, *, proposal=False, new_text=None):
    return [dict(candidate_id=c['candidate_id'], disposition='propose' if proposal else 'preserved',
                 source_evidence=record['source']['text'], proposed_text=new_text or audit.text_of(record), alternative_text='',
                 rationale='Compare the actual source forms and preserve the observed wording in this passage.')
            for c in audit.candidates(record)]


class DetectionAndGateTests(unittest.TestCase):
    def test_original_john_is_detected_without_looking_at_first_six_entries_only(self):
        d=ORIGINAL[0]
        self.assertEqual(d['lexical_decisions'][7]['source_word'], 'φιλῶ')
        found=audit.candidates(d)
        self.assertTrue(any(c['kind']=='source_form_collision' for c in found))
        self.assertTrue(any(c['kind']=='existing_note_signal' for c in found))
        self.assertTrue(audit.approved_errors(d))

    def test_old_high_agreement_empty_issues_is_not_accepted(self):
        with self.assertRaisesRegex(ValueError, 'source_distinction_checks'):
            audit.review_gate(ORIGINAL[0], {'agreement_score':1.0, 'verdict':'agree', 'issues':[]})
        with self.assertRaisesRegex(ValueError, 'Unreviewed'):
            audit.validate_checks(ORIGINAL[0], [])

    def test_all_three_approved_verses_pass_and_reverts_fail(self):
        for n in (15,16,17):
            d=approved(n)
            self.assertEqual(audit.approved_errors(d), [])
            self.assertFalse(audit.validate_checks(d,checks(d))['requires_maintainer_review'])
            with self.assertRaises(ValueError):
                audit.assert_approved(d,audit.text_of(d).replace('agape-love','love').replace('phileo-love','love'))

    def test_wrong_third_question_and_unqualified_extra_love_fail(self):
        d=approved(17)
        self.assertTrue(audit.approved_errors(d,audit.text_of(d).replace('do you phileo-love','do you agape-love')))
        self.assertTrue(audit.approved_errors(d,audit.text_of(d)+' I love you.'))

    def test_proposals_are_retained_and_quarantined_from_automatic_issues(self):
        d=ORIGINAL[0]; c=checks(d,proposal=True,new_text=audit.text_of(approved()))
        review=audit.review_gate(d,{'agreement_score':1.0,'verdict':'agree','issues':[], 'source_distinction_checks':c})
        self.assertTrue(review['requires_maintainer_review'])
        self.assertEqual(review['issues'], [])
        self.assertTrue(review['held_issues'])
        self.assertEqual(review['held_issues'][0]['suggested_rewrite'],audit.text_of(approved()))
        self.assertLess(review['agreement_score'],1.0)
        self.assertNotEqual(review['verdict'],'agree')
        with tempfile.TemporaryDirectory() as directory:
            path=audit.save_pending(d,review['source_distinction_audit'],Path(directory))
            self.assertIn('state/source_distinction_proposals',str(path))
            self.assertEqual(json.loads(path.read_text())['audit']['checks'],c)

    def test_hebrew_collision_is_a_review_lead_not_an_automatic_semantic_decision(self):
        d={'id':'TST.1.1','source':{'text':'ראה נבט'},'translation':{'text':'He looked and looked.'},
           'lexical_decisions':[{'source_word':'ראה','chosen':'looked'},{'source_word':'נבט','chosen':'looked'}]}
        found=audit.candidates(d);self.assertEqual(len(found),1)
        self.assertEqual(found[0]['kind'],'source_form_collision')
        c=checks(d);c[0]['disposition']='retain_after_comparison';c[0]['alternative_text']='He saw and looked.'
        self.assertFalse(audit.validate_checks(d,c)['requires_maintainer_review'])

    def test_inflected_forms_can_be_retained_after_explicit_comparison(self):
        d={'id':'TST.1.2','source':{'text':'λέγει εἶπεν'},'translation':{'text':'He said; he said.'},
           'lexical_decisions':[{'source_word':'λέγει','chosen':'said'},{'source_word':'εἶπεν','chosen':'said'}]}
        c=checks(d);self.assertEqual(len(c),1);c[0]['disposition']='retain_after_comparison';c[0]['alternative_text']='He says; he said.'
        self.assertFalse(audit.validate_checks(d,c)['requires_maintainer_review'])

    def test_retained_collision_cannot_close_without_a_full_english_alternative(self):
        d={'id':'TST.1.5','source':{'text':'ראה נבט'},'translation':{'text':'He looked and looked.'},
           'lexical_decisions':[{'source_word':'ראה','chosen':'looked'},{'source_word':'נבט','chosen':'looked'}]}
        c=checks(d)
        with self.assertRaisesRegex(ValueError,'explicit alternative'):
            audit.validate_checks(d,c)
        c[0]['disposition']='retain_after_comparison'
        with self.assertRaisesRegex(ValueError,'alternative_text'):
            audit.validate_checks(d,c)
        c[0]['alternative_text']='He saw and looked.'
        self.assertFalse(audit.validate_checks(d,c)['requires_maintainer_review'])

    def test_first_draft_discovery_does_not_require_predicting_a_future_hash(self):
        d={'id':'TST.1.6','source':{'text':'ראה נבט'},'translation':{'text':'He looked and looked.'},
           'lexical_decisions':[{'source_word':'ראה','chosen':'looked'},{'source_word':'נבט','chosen':'looked'}]}
        c=[dict(candidate_id='model-discovery:two-verbs',disposition='retain_after_comparison',
                source_evidence='ראה נבט',proposed_text=audit.text_of(d),alternative_text='He saw and looked.',
                rationale='Compare the two actual source forms and the full English alternatives.')]
        bound,bindings=audit.bind_draft_checks(d,c)
        self.assertEqual(len(bindings),1)
        self.assertEqual(c[0]['candidate_id'],'model-discovery:two-verbs')
        self.assertFalse(audit.validate_checks(d,bound)['requires_maintainer_review'])
        c[0]['source_evidence']='ראה'
        bound,bindings=audit.bind_draft_checks(d,c)
        self.assertEqual(bindings,{})
        with self.assertRaisesRegex(ValueError,'Unreviewed'):
            audit.validate_checks(d,bound)

    def test_one_phrase_level_lexical_decision_is_not_a_collision(self):
        d={'id':'TST.1.4','source':{'text':'בְּרֵאשִׁית בָּרָא'},'translation':{'text':'At the beginning he created.'},
           'lexical_decisions':[{'source_word':'בְּרֵאשִׁית בָּרָא','chosen':'created'}]}
        self.assertEqual(audit.candidates(d),[])

    def test_policy_is_scoped_not_a_global_love_replacement(self):
        d={'id':'JHN.3.35','source':{'text':'ἀγαπᾷ'},'translation':{'text':'The Father loves the Son.'}}
        self.assertEqual(audit.approved_errors(d),[])
        self.assertEqual(audit.candidates(d),[])
        self.assertFalse(audit.validate_checks(d,[])['requires_maintainer_review'])

    def test_missing_duplicate_and_fabricated_evidence_rejected(self):
        d=approved();c=checks(d)
        for bad in (c+c, [{**c[0],'source_evidence':'invented evidence'}], [{**c[0],'rationale':''}]):
            with self.assertRaises(ValueError):audit.validate_checks(d,bad)
        with self.assertRaises(ValueError):audit.validate_checks(d,[{**c[0],'proposed_text':'different full English wording not preserved'}])

    def test_non_greek_hebrew_source_evidence_remains_supported(self):
        d={'id':'TST.1.3','source':{'text':'amo diligo'},'translation':{'text':'I love and love.'}}
        c=[dict(candidate_id='model-discovery:latin-love',disposition='retain_after_comparison',
                source_evidence='amo diligo',proposed_text=audit.text_of(d),alternative_text='I love and cherish.',rationale='Compare the two source forms within the supplied context.')]
        self.assertFalse(audit.validate_checks(d,c)['requires_maintainer_review'])


class PipelineTests(unittest.TestCase):
    def test_first_draft_gate_runs_before_any_canonical_write(self):
        d=approved(); verse=SimpleNamespace(book_code='JHN',book_slug='john',chapter=21,verse=15,
                                            canonical_id=d['id'],reference=d['reference'],greek_text=d['source']['text'])
        tool=dict(english_text=audit.text_of(d),translation_philosophy='optimal-equivalence',
                  lexical_decisions=d['lexical_decisions'],footnotes=d['translation']['footnotes'],
                  source_distinction_checks=checks(d))
        with patch.object(draft,'build_user_prompt',return_value='fixture user prompt'),patch.object(draft,'source_distinction_prompt',return_value='fixture context'),patch.object(draft,'call_model',return_value=(tool,'fixture-model','{}',0.2)),patch.object(draft,'write_verse_yaml') as write:
            result=draft.draft_verse(verse,write=False)
            self.assertIn(audit.VERSION,result.record['ai_draft']['prompt_id'])
            self.assertTrue(audit.receipt_is_current(result.record))
            write.assert_not_called()
            broken=copy.deepcopy(tool);broken.pop('source_distinction_checks')
            with patch.object(draft,'call_model',return_value=(broken,'fixture-model','{}',0.2)):
                with self.assertRaisesRegex(ValueError,'source_distinction_checks'):
                    draft.draft_verse(verse,write=True)
            write.assert_not_called()

    def test_existing_receipt_is_invalidated_by_a_text_edit(self):
        d=approved();d['source_distinction_audit']=audit.validate_checks(d,checks(d))
        self.assertTrue(audit.receipt_is_current(d))
        d['translation']['text']+=' A later edit.'
        self.assertFalse(audit.receipt_is_current(d))

    def test_direct_writers_retain_proposals_without_overwriting_verses(self):
        for module,method in ((azure,'call_azure'),(gemini,'call_gemini')):
            with self.subTest(module=module.__name__),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);path=root/'015.yaml';path.write_text(yaml.safe_dump(ORIGINAL[0],allow_unicode=True));before=path.read_bytes()
                response={'revised_text':audit.text_of(ORIGINAL[0]),'unchanged':True,'changes_summary':'Compare source wording.',
                          'source_distinction_checks':checks(ORIGINAL[0],proposal=True,new_text=audit.text_of(approved()))}
                with patch.object(module,method,return_value=response) as call,patch.object(module,'REPO_ROOT',root):
                    out=module.revise_verse(path,'endpoint','key') if module is azure else module.revise_verse(path,'key')
                self.assertEqual(out['status'],'review_required')
                self.assertTrue(Path(out['proposal_path']).is_file())
                self.assertEqual(before,path.read_bytes())
                self.assertIn('φιλῶ',call.call_args.kwargs['context_block'])

    def test_actual_draft_and_revision_schemas_require_explicit_checks(self):
        for schema in (draft.SUBMIT_TOOL['function']['parameters'],azure.REVISION_TOOL['function']['parameters'],reviewer.RESPONSE_SCHEMA):
            self.assertIn('source_distinction_checks',schema['required'])
        for tool in agentic.TOOL_SCHEMAS:
            if tool['name'] in {'submit_revision','submit_unchanged'}:
                self.assertIn('source_distinction_checks',tool['input_schema']['required'])
        self.assertNotIn('additionalProperties',reviewer.RESPONSE_SCHEMA['properties']['source_distinction_checks']['items'])

    def test_all_loaded_system_routes_have_the_new_contract(self):
        for prompt in (draft.SYSTEM_PROMPT,azure.SYSTEM_PROMPT,gemini.SYSTEM_PROMPT,agentic.load_system_prompt()):
            self.assertIn('source_distinction_checks',prompt)
            self.assertNotIn('Every verse you leave alone is a verse you have validated',prompt)

    def test_missing_context_is_disclosed_and_neighbors_are_supplied(self):
        self.assertIn('unavailable',audit.context_block(None))
        path=ROOT/'translation/nt/john/021/015.yaml'
        context=audit.context_block(path)
        self.assertIn('JHN.21.17',context)
        self.assertIn('φιλεῖς',context)

    def test_actual_review_request_injects_contract_and_fingerprints_it(self):
        d=approved(); response=dict(agreement_score=1,verdict='agree',issues=[],notes='',source_distinction_checks=checks(d))
        body={'modelVersion':'fixture-model','candidates':[{'content':{'parts':[{'text':json.dumps(response)}]}}]}
        with patch.dict(os.environ,{'GOOGLE_APPLICATION_CREDENTIALS':''}),patch.object(reviewer,'_gemini_endpoint',return_value=('https://example.invalid/review',{})),patch.object(reviewer.urllib.request,'urlopen') as request:
            request.return_value.__enter__.return_value.read.return_value=json.dumps(body).encode()
            result,model=reviewer.call_gemini_review(yaml.safe_dump(d,allow_unicode=True),model='fixture',context_block='Provided neighboring source: φιλεῖς με.',retries=1)
            payload=json.loads(request.call_args.args[0].data)
            self.assertIn('source_distinction_checks',payload['systemInstruction']['parts'][0]['text'])
            self.assertIn('Provided neighboring source',payload['contents'][0]['parts'][0]['text'])
            self.assertNotIn('Passage context unavailable',payload['contents'][0]['parts'][0]['text'])
            self.assertEqual(model,'fixture-model')
            self.assertRegex(result['prompt_provenance']['system_sha256'],r'^[a-f0-9]{64}$')

    def test_actual_review_call_rejects_legacy_response_before_completion(self):
        body={'modelVersion':'fixture','candidates':[{'content':{'parts':[{'text':json.dumps(dict(agreement_score=1,verdict='agree',issues=[],notes='Standard and defensible.'))}]}}]}
        with patch.dict(os.environ,{'GOOGLE_APPLICATION_CREDENTIALS':''}),patch.object(reviewer,'_gemini_endpoint',return_value=('https://example.invalid/review',{})),patch.object(reviewer.urllib.request,'urlopen') as request:
            request.return_value.__enter__.return_value.read.return_value=json.dumps(body).encode()
            with self.assertRaisesRegex(ValueError,'source_distinction_checks'):
                reviewer.call_gemini_review(yaml.safe_dump(ORIGINAL[0],allow_unicode=True),model='fixture',retries=1)
            self.assertEqual(request.call_count,1)

    def test_generic_high_scrutiny_no_longer_has_zero_context(self):
        job=dict(testament='nt',book_slug='john',chapter=21,verse=15,model='fixture',strategy='high_scrutiny',id=1)
        d=approved();response=audit.review_gate(d,dict(agreement_score=1,verdict='agree',issues=[],notes='',source_distinction_checks=checks(d)))
        response['prompt_provenance']={'fixture':True}
        with tempfile.TemporaryDirectory(dir=ROOT) as directory, patch.object(reviewer,'REVIEWS_DIR',Path(directory)), patch.object(reviewer,'REPO_ROOT',ROOT), patch.object(reviewer,'mark_complete'), patch.object(reviewer,'call_gemini_review',return_value=(response,'fixture-model')) as call:
            # review_output_path normally lives under REPO_ROOT; keep relative paths valid.
            with patch.object(reviewer,'review_output_path',return_value=Path(directory)/'test-distinction-review.json'):
                try:
                    result=reviewer.run_job(None,job)
                    self.assertIn('φιλεῖς',call.call_args.kwargs['context_block'])
                    self.assertGreater(result['context_window_verses'],0)
                    self.assertIn(audit.VERSION,result['prompt_version'])
                finally:
                    (Path(directory)/'test-distinction-review.json').unlink(missing_ok=True)

    def test_both_direct_revision_writers_cannot_silently_accept_original(self):
        for module,method in ((azure,'call_azure'),(gemini,'call_gemini')):
            with self.subTest(module=module.__name__),tempfile.TemporaryDirectory() as directory:
                path=Path(directory)/'015.yaml';path.write_text(yaml.safe_dump(ORIGINAL[0],allow_unicode=True));before=path.read_bytes()
                result={'revised_text':audit.text_of(ORIGINAL[0]),'unchanged':True,'changes_summary':'No changes needed.'}
                fn=module.revise_verse
                with patch.object(module,method,return_value=result):
                    out=fn(path,'endpoint','key') if module is azure else fn(path,'key')
                self.assertIn('error',out)
                self.assertEqual(path.read_bytes(),before)

    def test_unflagged_text_issue_cannot_bypass_audit_quarantine(self):
        d=approved()
        response=audit.review_gate(d,dict(agreement_score=1,verdict='agree',source_distinction_checks=checks(d),
            issues=[dict(target='translation_text',suggested_rewrite='love',current_rendering='agape-love')]))
        self.assertTrue(response['requires_maintainer_review'])
        self.assertEqual(response['issues'],[])
        self.assertEqual(response['source_distinction_audit']['held_issues'],response['held_issues'])

    def test_source_proposal_issues_never_auto_apply(self):
        issue={'source_distinction_proposal':True,'target':'translation_text','severity':'minor','category':'grammar',
               'current_rendering':'love','suggested_rewrite':'agape-love','rationale':'ἀγαπᾷς'}
        self.assertEqual(auto.classify_issue(issue,ORIGINAL[0])[0],3)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/'review.json';p.write_text(json.dumps({'requires_maintainer_review':True,'issues':[issue]}))
            with patch.object(auto,'REPO_ROOT',root),patch.object(auto,'update_processing_state') as update:
                out=auto.process_review_job(None,{'review_path':'review.json','id':1},enabled_tiers={1,2,3},dry_run=False)
                self.assertEqual(out['applied'],0)
                self.assertEqual(update.call_args.kwargs['process_status'],'manual_review_required')

    def test_auto_apply_writer_rejects_flattening(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'015.yaml';p.write_text(yaml.safe_dump(approved(),allow_unicode=True));before=p.read_bytes()
            with self.assertRaises(ValueError):
                auto.apply_revision_to_yaml(p,find='agape-love',replace='love',rationale='fixture',review_path='fixture',category='lexical',tier=1)
            self.assertEqual(before,p.read_bytes())

    def test_spob_validator_rejects_approved_wording_regression(self):
        with tempfile.TemporaryDirectory() as directory:
            d=yaml.safe_load((ROOT/'translation_simplified/nt/john/021/015.yaml').read_text())
            d['translation']['text']=d['translation']['text'].replace('agape-love','love')
            p=Path(directory)/'015.yaml';p.write_text(yaml.safe_dump(d,allow_unicode=True))
            self.assertTrue(any('approved love-word sequence' in e for e in spob.validate_simplified_record(p)))


if __name__=='__main__':unittest.main()
