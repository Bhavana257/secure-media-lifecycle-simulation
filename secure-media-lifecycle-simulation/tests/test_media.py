import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from media_lab import init,sanitize,verify,workspace_dir
class MediaTests(unittest.TestCase):
 def test_roundtrip(self):
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp); init(folder,4)
   self.assertFalse(verify(folder))
   self.assertTrue(sanitize(folder,'Tester')['verified_zero'])
   self.assertTrue(verify(folder))
 def test_reject_overwrite(self):
  with tempfile.TemporaryDirectory() as tmp:
   folder=Path(tmp); init(folder,4)
   with self.assertRaises(FileExistsError): init(folder,4)
 def test_reject_traversal(self):
  with self.assertRaises(ValueError): workspace_dir('../outside')
