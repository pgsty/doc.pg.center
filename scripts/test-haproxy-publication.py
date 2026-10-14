#!/usr/bin/env python3
"""HAProxy gate mutation tests using external copies of actual publication inputs.

All tests call the publication gate as a subprocess. Mutations replace files in
isolated fixtures; hardlinked rendered artifacts are never modified in place.
A PASS demonstrates a detected defect, except positive French-label controls.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

DEFAULT_ROOT = Path.cwd()
FIXTURE_MARKER = '.haproxy-publication-fixture'
ENGLISH = 'The server will not accept a connection when the request is invalid.'
FRENCH = 'Les mots-clés « for », « by », « with », « on », « in » et « to » sont des paramètres de syntaxe HAProxy.'


def replace_file(path, text):
    # Essential: fixture outputs are hardlinks; detach before any write.
    if path.exists(): path.unlink()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def linktree(source, target):
    shutil.copytree(source, target, copy_function=os.link, ignore=shutil.ignore_patterns('__pycache__'))


def ledger_refresh(root, name):
    path=root/'data/translation-audits/haproxy.json'
    data=json.loads(path.read_text())
    for pair in data['pairs']:
        if pair['target']==f'content/docs/haproxy/{name}.fr.md':
            pair['target_sha256']=digest(root/pair['target'])
    replace_file(path, json.dumps(data, ensure_ascii=False, indent=2)+'\n')


def setup_fixture(repo, public, work):
    if work.exists():
        if any(work.iterdir()) and not (work/FIXTURE_MARKER).is_file():
            raise ValueError('Refusing to replace a nonempty output directory without the fixture ownership marker')
        shutil.rmtree(work)
    work.mkdir(parents=True)
    (work/FIXTURE_MARKER).write_text('Created by the HAProxy publication regression helper.\n')
    base=work/'baseline'
    for directory in ('scripts','content','data','layouts','assets','static','i18n','sources'):
        shutil.copytree(repo/directory, base/directory, ignore=shutil.ignore_patterns('__pycache__'))
    for name in ('hugo.yaml','go.mod','go.sum'):
        shutil.copy2(repo/name,base/name)
    config=base/'hugo.yaml'
    config.write_text(re.sub(r'^enableGitInfo: true$', 'enableGitInfo: false', config.read_text(), flags=re.M))
    linktree(public, work/'rendered-baseline')
    return base


def run_gate(root, output=None):
    args=[sys.executable,str(root/'scripts/check-haproxy.py')]
    if output: args+=['--rendered-dir',str(output)]
    started=time.monotonic()
    result=subprocess.run(args,cwd=root,capture_output=True,text=True)
    return {'exit_code':result.returncode,'seconds':round(time.monotonic()-started,3),'output':result.stdout+result.stderr}


def clone_source(base, work, name):
    root=work/name/'repo'
    linktree(base,root)
    return root


def clone_output(work, name):
    output=work/name/'public'
    linktree(work/'rendered-baseline',output)
    return output


def mutate_text(root, name, transform, refresh=True):
    target=root/f'content/docs/haproxy/{name}.fr.md'
    replace_file(target, transform(target.read_text()))
    if refresh: ledger_refresh(root,name)


def paragraph(text):
    # A genuine source paragraph without code, metadata or references.
    body=text.split('\n---\n',1)[1]
    return next(p for p in body.split('\n\n') if p.startswith('HAProxy est conçu'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,default=DEFAULT_ROOT)
    parser.add_argument('--public','--rendered-dir',dest='public',type=Path,required=True)
    parser.add_argument('--work','--output-dir',dest='work',type=Path,required=True)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args()
    args.repo=args.repo.resolve();args.public=args.public.resolve();args.work=args.work.resolve()
    args.report=(args.report or args.work/'results.json').resolve()
    if args.work.is_relative_to(args.repo) or args.repo.is_relative_to(args.work) or args.report.is_relative_to(args.repo):
        parser.error('Fixture output must not overlap the repository; report paths must be outside it')
    if args.report.is_relative_to(args.public):
        parser.error('Report path must not overwrite the existing rendered output')
    if args.public.is_relative_to(args.work) or args.work.is_relative_to(args.public):
        parser.error('Fixture output must be separate from the existing rendered output')
    args.report.parent.mkdir(parents=True,exist_ok=True)
    base=setup_fixture(args.repo,args.public,args.work)
    results=[]
    baseline=run_gate(base,args.work/'rendered-baseline')
    results.append({'test':'complete_current_baseline','expected':'pass',**baseline,'passed':baseline['exit_code']==0})
    if baseline['exit_code']:
        args.report.write_text(json.dumps({'results':results,'blocked':'Baseline publication gate is not green; mutation claims would be confounded.'},ensure_ascii=False,indent=2)+'\n')
        print(baseline['output']);return 2
    def test(name, modify, expected, needles=(), rendered=False):
        root=clone_source(base,args.work,name)
        output=clone_output(args.work,name) if rendered else None
        modify(root,output)
        result=run_gate(root,output)
        passed=(result['exit_code']==0)==(expected=='pass')
        if needles: passed=passed and all(n in result['output'] for n in needles)
        results.append({'test':name,'expected':expected,'passed':passed,**result})
        print(f'{name}: '+('PASS' if passed else 'GAP')+'; '+str(result['exit_code']),flush=True)
    def checksum_corruption(root,output):
        path=root/'sources/haproxy/upstream/intro.txt'
        replace_file(path,path.read_text()+'\nUnreviewed upstream source mutation.\n')
    test('pinned_upstream_checksum_corruption',checksum_corruption,'fail',('pinned upstream checksum changed: intro.txt',))
    def duplicate_source_file(root,output):
        path=root/'sources/haproxy/SNAPSHOT.json';payload=json.loads(path.read_text())
        # Preserve the record count and all recorded digests: uniqueness and
        # complete input coverage must catch a duplicated path on their own.
        payload['files'][-1]=dict(payload['files'][0])
        replace_file(path,json.dumps(payload,ensure_ascii=False))
    test('duplicate_pinned_source_file_entry',duplicate_source_file,'fail',('snapshot must include all seven original input files exactly once',))
    def stable_release_metadata(root,output):
        path=root/'data/translation-audits/haproxy.json';payload=json.loads(path.read_text())
        payload['stable_release']='3.4.7';payload['stable_tag']='v3.4.7'
        replace_file(path,json.dumps(payload,ensure_ascii=False))
    test('wrong_stable_release_with_current_documentation_hashes',stable_release_metadata,'fail',('publication ledger stable release/tag differs',))
    def documentation_ref_metadata(root,output):
        path=root/'data/translation-audits/haproxy.json';payload=json.loads(path.read_text())
        payload['upstream_ref']='v3.4.4'
        replace_file(path,json.dumps(payload,ensure_ascii=False))
    test('stale_documentation_ref_with_current_hashes',documentation_ref_metadata,'fail',('publication ledger documentation ref differs',))
    def pair_version_metadata(root,output):
        path=root/'data/translation-audits/haproxy.json';payload=json.loads(path.read_text())
        next(p for p in payload['pairs'] if p['language']=='fr')['documentation_version']='3.4.4'
        replace_file(path,json.dumps(payload,ensure_ascii=False))
    test('stale_pair_version_with_current_review_hashes',pair_version_metadata,'fail',('publication pair documentation version differs',))
    def sample_return_type(root,output):
        mutate_text(root,'acls-and-samples',lambda t:t.replace('url_port : integer','url_port : string',1))
    test('wrong_unfenced_sample_return_type_after_ledger_rehash',sample_return_type,'fail',('unfenced sample return type signatures differ',))
    def deprecated_alias(root,output):
        mutate_text(root,'acls-and-samples',lambda t:t.replace('req_ssl_hello_type : integer','req.ssl_hello_type : integer',1))
    test('wrong_deprecated_sample_alias_after_ledger_rehash',deprecated_alias,'fail',('unfenced sample return type signatures differ',))
    def command(root,output):
        mutate_text(root,'security',lambda t:t.replace('user haproxy\ngroup haproxy','user root\ngroup haproxy',1))
    test('unreviewed_command_even_after_ledger_rehash',command,'fail',('fenced code or literal output changed without a prose review',))
    def mixed_command(root,output):
        name='statistics-and-monitoring'
        mutate_text(root,name,lambda t:t.replace('> abusers-ip.txt','> banned-ip.txt',1))
        target=root/f'content/docs/haproxy/{name}.fr.md'
        blocks=list(re.finditer(r'^```[^\n]*\n.*?^```[ \t]*(?:\n|$)',target.read_text(),re.M|re.S))
        manifest=root/f'data/translation-fences/haproxy.fr/{name}.json';payload=json.loads(manifest.read_text())
        entry=next(e for e in payload['fences'] if any('abusers-ip.txt' in line for line in e.get('protected_lines',[])))
        entry['target_sha256']=hashlib.sha256(blocks[entry['index']-1].group(0).encode()).hexdigest()
        replace_file(manifest,json.dumps(payload,ensure_ascii=False))
    test('protected_command_in_mixed_fence_after_all_hash_rebase',mixed_command,'fail',('protected code/output line changed',))
    def metadata(root,output):
        path=root/'data/translation-audits/haproxy.json';payload=json.loads(path.read_text());payload['pairs'].pop()
        replace_file(path,json.dumps(payload,ensure_ascii=False))
    test('omitted_publication_pair_metadata',metadata,'fail',('all 190 translation pairs',))
    def scope_metadata(root,output):
        path=root/'data/translation-audits/haproxy.json';payload=json.loads(path.read_text())
        next(p for p in payload['pairs'] if p['language']=='fr').pop('review_scope')
        replace_file(path,json.dumps(payload,ensure_ascii=False))
    test('omitted_publication_review_scope',scope_metadata,'fail',('missing publication review scope',))
    def explanation_note(root,output):
        path=root/'data/translation-fences/haproxy.fr/filters.json';payload=json.loads(path.read_text());payload['fences'][0].pop('review')
        replace_file(path,json.dumps(payload,ensure_ascii=False))
    test('omitted_explanation_review_note',explanation_note,'fail',('review',))
    def explanation_meta(root,output):
        path=root/'data/translation-fences/haproxy.fr/filters.json';payload=json.loads(path.read_text());payload['fences'].pop(0)
        replace_file(path,json.dumps(payload,ensure_ascii=False))
    test('omitted_explanation_review_metadata',explanation_meta,'fail',('missing explanatory-fence translations',))
    def explanation_body(root,output):
        mutate_text(root,'filters',lambda t:re.sub(r'```text\n.*?\n```','```text\n```',t,count=1,flags=re.S))
    test('omitted_explanation_body',explanation_body,'fail',('differs from the reviewed translation',))
    def english_prose(root,output):
        mutate_text(root,'security',lambda t:t.replace(paragraph(t),ENGLISH,1))
    test('ordinary_english_prose',english_prose,'fail',('probable untranslated prose',))
    def french_labels(root,output):
        mutate_text(root,'security',lambda t:t.replace(paragraph(t),FRENCH,1))
    test('quoted_french_syntax_labels',french_labels,'pass')
    def english_fence(root,output):
        mutate_text(root,'filters',lambda t:t.replace('```text\n','```text\n'+ENGLISH+'\n',1))
        target=root/'content/docs/haproxy/filters.fr.md'
        block=re.search(r'```text\n.*?\n```\n',target.read_text(),re.S).group(0)
        path=root/'data/translation-fences/haproxy.fr/filters.json';data=json.loads(path.read_text());data['fences'][0]['target_sha256']=hashlib.sha256(block.encode()).hexdigest()
        replace_file(path,json.dumps(data,ensure_ascii=False))
    test('english_prose_in_reviewed_explanation_fence',english_fence,'fail',('probable untranslated prose',))
    def markdown_truncation(root,output):
        path=output/'fr/docs/haproxy/security/index.md';replace_file(path,path.read_text().replace(paragraph((root/'content/docs/haproxy/security.fr.md').read_text()),'',1))
    test('exported_markdown_body_truncation',markdown_truncation,'fail',('complete Markdown body',),True)
    def llms_truncation(root,output):
        path=output/'fr/docs/haproxy/llms-full.txt';replace_file(path,path.read_text().replace(paragraph((root/'content/docs/haproxy/security.fr.md').read_text()),'',1))
    test('exported_llms_body_truncation',llms_truncation,'fail',('complete LLMS body',),True)
    def shared_html_truncation(root,output):
        normal=output/'fr/docs/haproxy/security/index.html'
        matches=list(re.finditer(r'<p\b[^>]*>HAProxy est conçu.*?</p>',normal.read_text(),re.S))
        if len(matches)!=1:raise RuntimeError('Expected one security paragraph in normal HTML')
        block=matches[0].group(0)
        for path in (normal,output/'fr/_print/docs/haproxy/index.html'):
            text=path.read_text()
            if text.count(block)!=1:raise RuntimeError(f'Expected one identical security paragraph in {path}')
            replace_file(path,text.replace(block,'',1))
    test('matching_normal_and_print_html_body_truncation',shared_html_truncation,'fail',('HTML body differs from independently rendered source',),rendered=True)
    def shared_html_code(root,output):
        for path in (output/'fr/docs/haproxy/security/index.html',output/'fr/_print/docs/haproxy/index.html'):
            text=path.read_text();matches=[m for m in re.finditer(r'<pre\b.*?</pre>',text,re.S) if 'user haproxy' in re.sub('<[^>]+>','',m.group(0)) and 'group haproxy' in re.sub('<[^>]+>','',m.group(0))]
            if len(matches)!=1:raise RuntimeError(f'Expected one security config pre in {path}, found {len(matches)}')
            replace_file(path,text[:matches[0].start()]+text[matches[0].end():])
    test('matching_normal_and_print_html_code_omission',shared_html_code,'fail',('HTML body differs from independently rendered source','missing or changed rendered fence'),rendered=True)
    def shared_html_heading(root,output):
        for path in (output/'fr/docs/haproxy/security/index.html',output/'fr/_print/docs/haproxy/index.html'):
            text=path.read_text();matches=[m for m in re.finditer(r'<h2\b[^>]*>.*?</h2>',text,re.S) if 'Prise en charge des capacités Linux' in m.group(0)]
            if len(matches)!=1:raise RuntimeError(f'Expected one Linux capabilities heading in {path}')
            block=matches[0].group(0);changed=block.replace('Prise en charge des capacités Linux','Linux capabilities support')
            replace_file(path,text.replace(block,changed,1))
    test('matching_normal_and_print_html_heading_corruption',shared_html_heading,'fail',('HTML heading text differs from source','print heading text differs from source'),rendered=True)
    def shared_html_title(root,output):
        for path in (output/'fr/docs/haproxy/security/index.html',output/'fr/_print/docs/haproxy/index.html'):
            text=path.read_text();matches=[m for m in re.finditer(r'<h1\b[^>]*>.*?</h1>',text,re.S) if 'Considérations de sécurité' in m.group(0)]
            if len(matches)!=1:raise RuntimeError(f'Expected one security page title in {path}')
            block=matches[0].group(0);changed=block.replace('Considérations de sécurité','Security considerations')
            replace_file(path,text.replace(block,changed,1))
    test('matching_normal_and_print_html_title_corruption',shared_html_title,'fail',('localized HTML page title differs from front matter','localized print page title differs from front matter'),rendered=True)
    report={'fixture_policy':'Complete source copies including all Hugo inputs; hardlinked fixture outputs are unlinked before writing; live repository/build untouched. Copied hugo.yaml disables Git metadata because the standalone fixture has no history.','baseline_repo':str(args.repo),'baseline_public':str(args.public),'checker_sha256':{name:digest(base/'scripts'/name) for name in ('check-haproxy.py','check-component-translations.py','translation_fences.py')},'results':results,'gaps':[r['test'] for r in results if not r['passed']]}
    args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    return 1 if report['gaps'] else 0
if __name__=='__main__':raise SystemExit(main())
