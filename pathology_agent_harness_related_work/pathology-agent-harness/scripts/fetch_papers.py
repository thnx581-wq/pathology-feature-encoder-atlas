#!/usr/bin/env python3
"""Fetch pinned arXiv papers. Standard library, Python 3.10+; no code execution.
Usage: --list | --all | --paper react
Failures are recorded; they never imply the author made a PDF-only submission.
"""
from __future__ import annotations
import argparse, gzip, hashlib, io, json, re, shutil, tarfile, tempfile, time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any
ROOT = Path(__file__).resolve().parents[1]
MAX_DOWNLOAD = 100 * 1024 * 1024
MAX_EXPANDED = 200 * 1024 * 1024
STALE = {'history','old','backup','draft','previous','archive','submitted'}

def dump(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def valid_pdf(data: bytes) -> bool:
    return data.startswith(b'%PDF-') and b'%%EOF' in data[-8192:]

def safe_target(root: Path, name: str) -> Path:
    if '\x00' in name or '\\' in name or ':' in name:
        raise ValueError('Unsafe archive path')
    rel=PurePosixPath(name)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('Unsafe archive path')
    target=root.joinpath(*rel.parts)
    target.resolve().relative_to(root.resolve())
    return target

def unpack_source(blob: bytes, dest: Path) -> str:
    dest.mkdir(parents=True,exist_ok=True)
    try:
        archive=tarfile.open(fileobj=io.BytesIO(blob),mode='r:*')
    except tarfile.ReadError:
        if blob[:2]==b'\x1f\x8b':
            with gzip.GzipFile(fileobj=io.BytesIO(blob)) as stream:
                data=stream.read(MAX_EXPANDED+1)
        else: data=blob
        if len(data)>MAX_EXPANDED: raise ValueError('Expanded file exceeds limit')
        text=data.decode('utf-8',errors='replace')
        if '<html' in text[:2000].lower() or not re.search(r'\\(documentclass|documentstyle|begin\s*\{document\})',text):
            raise ValueError('Not a recognized TeX source file/archive')
        (dest/'main.tex').write_bytes(data)
        return 'single_tex'
    with archive:
        total=0
        seen=set()
        for i,member in enumerate(archive):
            if i>=5000: raise ValueError('Too many archive entries')
            target=safe_target(dest,member.name)
            if member.isdir(): target.mkdir(parents=True,exist_ok=True); continue
            if not member.isfile(): raise ValueError('Archive links/special files forbidden')
            key=str(target.resolve())
            if key in seen: raise ValueError('Duplicate archive entry')
            seen.add(key)
            total+=member.size
            if total>MAX_EXPANDED: raise ValueError('Expanded archive exceeds limit')
            target.parent.mkdir(parents=True,exist_ok=True)
            source=archive.extractfile(member)
            if source is None: raise ValueError('Unreadable member')
            with source, target.open('xb') as out: shutil.copyfileobj(source,out)
    return 'tar_archive'

def strip_tex_comments(text: str) -> str:
    """Search-only cleaning, not a complete TeX parser. Preserve all originals."""
    result=[]
    verbatim=None
    for line in text.splitlines(keepends=True):
        if verbatim:
            result.append(line)
            if '\\end{'+verbatim+'}' in line: verbatim=None
            continue
        match=re.search(r'\\begin\{(verbatim\*?|lstlisting|minted)\}',line)
        if match:
            result.append(line)
            if '\\end{'+match.group(1)+'}' not in line: verbatim=match.group(1)
            continue
        if '\\verb' in line: result.append(line); continue
        stop=None
        for i,c in enumerate(line):
            if c!='%': continue
            n=0; j=i-1
            while j>=0 and line[j]=='\\': n+=1; j-=1
            if n%2==0: stop=i; break
        result.append(line if stop is None else line[:stop]+('\n' if line.endswith('\n') else ''))
    return ''.join(result)

def clean_source(root: Path) -> dict[str, Any]:
    moved=[]
    dirs=sorted((p for p in root.rglob('*') if p.is_dir()),key=lambda p:len(p.parts))
    for p in dirs:
        if not p.exists() or '.stale' in p.relative_to(root).parts: continue
        if p.name.lower() in STALE:
            rel=p.relative_to(root); dest=root/'.stale'/rel
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.move(str(p),str(dest)); moved.append(str(rel))
    cleaned=0
    for p in root.rglob('*.tex'):
        if '.stale' in p.relative_to(root).parts: continue
        original=p.with_name(p.name+'.orig')
        if not original.exists(): shutil.copyfile(p,original)
        try: text=original.read_bytes().decode('utf-8')
        except UnicodeDecodeError: continue
        p.write_text(strip_tex_comments(text),encoding='utf-8'); cleaned+=1
    return {'cleaned_tex_count':cleaned,'quarantined_directories':moved}

def download(url: str, dest: Path) -> None:
    request=urllib.request.Request(url,headers={'User-Agent':'pathology-literature-review/1.0 (academic use)'})
    try:
        with urllib.request.urlopen(request,timeout=90) as response, dest.open('wb') as out:
            total=0
            while chunk:=response.read(1024*1024):
                total+=len(chunk)
                if total>MAX_DOWNLOAD: raise ValueError('Download exceeds limit')
                out.write(chunk)
    finally: time.sleep(3)

def fetch_one(p: dict[str,Any]) -> bool:
    dest=ROOT/'related_work'/p['folder']
    status={'attempted_at_utc':datetime.now(timezone.utc).isoformat(),'arxiv_version':p['arxiv']+p['version'],
            'pdf':'NOT_DOWNLOADED','source':'NOT_DOWNLOADED'}
    with tempfile.TemporaryDirectory(prefix='arxiv-fetch-') as tmp:
        tmpdir=Path(tmp); pdf=dest/'paper.pdf'
        try:
            if pdf.exists():
                if not valid_pdf(pdf.read_bytes()): raise ValueError('Existing invalid PDF; inspect manually')
                status['pdf']='VALIDATED_EXISTING'
            else:
                fetched=tmpdir/'paper.download'; download(p['pdf_url'],fetched)
                if not valid_pdf(fetched.read_bytes()): raise ValueError('PDF header/EOF check failed; no paper.pdf written')
                shutil.copyfile(fetched,pdf); status['pdf']='DOWNLOADED_FORMAT_CHECKED'
            status['pdf_sha256']=hashlib.sha256(pdf.read_bytes()).hexdigest()
        except (OSError,ValueError) as error:
            status['pdf']='FETCH_FAILED'; status['pdf_error']=str(error)
        try:
            source=dest/'source'
            existing=[x for x in source.rglob('*.tex') if '.stale' not in x.parts]
            if existing: status['source']='EXISTING_TEX_NOT_OVERWRITTEN'
            else:
                archive_path=tmpdir/'source.download'; download(p['source_url'],archive_path)
                unpacked=tmpdir/'source'; kind=unpack_source(archive_path.read_bytes(),unpacked)
                status.update(clean_source(unpacked))
                for item in unpacked.rglob('*'):
                    if item.is_file() and (source/'upstream'/item.relative_to(unpacked)).exists():
                        raise ValueError('Local source conflict; refusing overwrite')
                shutil.copytree(unpacked,source/'upstream',dirs_exist_ok=True)
                shutil.copyfile(archive_path,dest/'source_archive.bin')
                status['source_archive_type']=kind
                status['source_sha256']=hashlib.sha256(archive_path.read_bytes()).hexdigest()
                status['source']='DOWNLOADED_TEX' if any(unpacked.rglob('*.tex')) else 'ARCHIVE_DOWNLOADED_NO_TEX_DETECTED'
        except (OSError,ValueError,tarfile.TarError,EOFError) as error:
            status['source']='FETCH_FAILED'; status['source_error']=str(error)
    dump(dest/'download_status.json',status)
    meta=json.loads((dest/'metadata.json').read_text(encoding='utf-8'))
    meta.update(pdf_local_status=status['pdf'],latex_local_status=status['source'],latest_download_record='download_status.json')
    dump(dest/'metadata.json',meta)
    (dest/'DOWNLOAD_STATUS.md').write_text('# 原文归档状态\n\n```json\n'+json.dumps(status,ensure_ascii=False,indent=2)+
        '\n```\n\n网络或格式失败不说明作者为 PDF-only 投稿。baseline 仍为 NOT_RUN。\n',encoding='utf-8')
    (dest/'source').mkdir(exist_ok=True)
    (dest/'source/README.md').write_text('# 源码状态\n\n'+str(status['source'])+
        '\n\n详见上一级 download_status.json。原始归档 source_archive.bin；作者文件保留在 upstream/，清理版仅供搜索，对照 .orig/PDF 核查。\n',encoding='utf-8')
    print(f"{p['id']}: PDF={status['pdf']}; source={status['source']}")
    return status['pdf']!='FETCH_FAILED' and status['source']!='FETCH_FAILED'

def main() -> int:
    path=ROOT/'related_work/manifest.json'; manifest=json.loads(path.read_text(encoding='utf-8'))
    parser=argparse.ArgumentParser(description=__doc__); group=parser.add_mutually_exclusive_group()
    group.add_argument('--list',action='store_true'); group.add_argument('--all',action='store_true')
    group.add_argument('--paper',choices=[p['id'] for p in manifest['papers']]); args=parser.parse_args()
    if not args.all and not args.paper:
        for p in manifest['papers']: print(p['id'],p['arxiv']+p['version'],p['title'])
        return 0
    ok=True
    for p in manifest['papers']:
        if args.all or args.paper==p['id']:
            ok=fetch_one(p) and ok
            p.update(json.loads((ROOT/'related_work'/p['folder']/'metadata.json').read_text(encoding='utf-8')))
            dump(path,manifest)
    return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
