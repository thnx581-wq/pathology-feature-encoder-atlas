#!/usr/bin/env python3
"""Offline tests, synthetic in-memory bytes only; no real paper files created."""
import io,tarfile,tempfile,unittest
from pathlib import Path
from fetch_papers import valid_pdf,safe_target,unpack_source,strip_tex_comments,clean_source
class Tests(unittest.TestCase):
 def test_pdf(self):
  self.assertTrue(valid_pdf(b'%PDF-1.7\nsynthetic-only\n%%EOF'))
  self.assertFalse(valid_pdf(b'<html>error</html>'));self.assertFalse(valid_pdf(b'%PDF-1.7\ntruncated'))
 def test_paths(self):
  for name in ['../bad','/bad','a/../../bad','C:/bad','a\\bad','a\x00b']:
   with self.assertRaises(ValueError):safe_target(Path('/tmp/example'),name)
 def test_comments(self):self.assertEqual(strip_tex_comments('x %old\ny \\% kept\n'),'x \ny \\% kept\n')
 def test_verbatim(self):
  s='\\begin{verbatim}\nx % keep\n\\end{verbatim}\n';self.assertEqual(strip_tex_comments(s),s)
 def test_inline_verb(self):
  s='\\verb|%| remains\n';self.assertEqual(strip_tex_comments(s),s)
 def test_html(self):
  with tempfile.TemporaryDirectory() as td:
   with self.assertRaises(ValueError):unpack_source(b'<html>rate limit</html>',Path(td))
 def test_single_tex(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);unpack_source(b'\\documentclass{article}\n',root);self.assertTrue((root/'main.tex').is_file())
 def test_tar_regular(self):
  b=io.BytesIO()
  with tarfile.open(fileobj=b,mode='w:gz') as t:
   data=b'\\documentclass{article}\n';i=tarfile.TarInfo('paper/main.tex');i.size=len(data);t.addfile(i,io.BytesIO(data))
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);unpack_source(b.getvalue(),root);self.assertTrue((root/'paper/main.tex').exists())
 def test_symlink(self):
  b=io.BytesIO()
  with tarfile.open(fileobj=b,mode='w') as t:
   i=tarfile.TarInfo('evil');i.type=tarfile.SYMTYPE;i.linkname='/etc/passwd';t.addfile(i)
  with tempfile.TemporaryDirectory() as td:
   with self.assertRaises(ValueError):unpack_source(b.getvalue(),Path(td))
 def test_stale_original(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);(root/'old').mkdir();(root/'old/main.tex').write_text('old');(root/'main.tex').write_text('x % old\n')
   result=clean_source(root);self.assertTrue((root/'.stale/old/main.tex').exists())
   self.assertEqual((root/'main.tex.orig').read_text(),'x % old\n');self.assertEqual((root/'main.tex').read_text(),'x \n')
   self.assertEqual(result['cleaned_tex_count'],1)
if __name__=='__main__':unittest.main(verbosity=2)
