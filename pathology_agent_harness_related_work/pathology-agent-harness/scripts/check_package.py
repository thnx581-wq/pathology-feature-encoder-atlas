#!/usr/bin/env python3
"""Offline structural checks, not a scientific reproduction test."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def main():
    errors=[]
    for name in ['README.md','AGENTS.md','handoff.md','brainstorm.md','dataset.md','experiment/evaluation.md',
                 'experiment/results.md','related_work/manifest.json','related_work/references.bib','related_work/00_survey.md']:
        if not (ROOT/name).is_file(): errors.append('Missing '+name)
    manifest=json.loads((ROOT/'related_work/manifest.json').read_text(encoding='utf-8'))
    pdfs=[]; sources=[]
    for p in manifest['papers']:
        d=ROOT/'related_work'/p['folder']
        for name in ['notes.md','metadata.json','DOWNLOAD_STATUS.md','source/README.md']:
            if not (d/name).is_file(): errors.append('Missing '+str(d/name))
        if not (d/'paper.pdf').exists(): pdfs.append(p['id'])
        elif not (d/'paper.pdf').read_bytes().startswith(b'%PDF-'): errors.append('Invalid PDF '+p['id'])
        if not list((d/'source').rglob('*.tex')): sources.append(p['id'])
        if p['arxiv']+p['version'] not in p['pdf_url']: errors.append('Version mismatch '+p['id'])
    for f in ROOT.rglob('*.md'):
        text=f.read_text(encoding='utf-8')
        if re.search(r'\{\{[^{}]+\}\}',text): errors.append('Unfilled template '+str(f))
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
            if '://' in target or target.startswith(('#','mailto:')): continue
            target=target.split('#')[0]
            if target and not (f.parent/target).exists(): errors.append(f'Broken link: {f.relative_to(ROOT)} -> {target}')
    print(json.dumps({'status':'PASS' if not errors else 'FAIL','paper_count':len(manifest['papers']),
      'missing_local_pdfs':pdfs,'missing_local_latex':sources,
      'meaning':'PASS is structure validation, not completed downloads or scientific experiments.','errors':errors},ensure_ascii=False,indent=2))
    return bool(errors)
if __name__=='__main__': raise SystemExit(main())
