import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_catalogue as verify

class CatalogueValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.root.mkdir(exist_ok=True)
        self.patch=patch.object(verify,'DATA',self.root)
        self.patch.start()
    def tearDown(self):
        self.patch.stop()
        self.tmp.cleanup()
    def write(self,card):
        (self.root/'index.json').write_text(json.dumps([{'id':'test-set','name':'Test'}]))
        (self.root/'test-set.json').write_text(json.dumps({'id':'test-set','cards':[card]}))
    def card(self):
        return {'pid':123,'name':'Example','num':'001/100','role':'main','prints':[{'t':'Normal','m':1.25}]}
    def test_valid(self):
        self.write(self.card())
        self.assertEqual(verify.validate(),[])
    def test_negative_price(self):
        card=self.card()
        card['prints'][0]['m']=-1
        self.write(card)
        self.assertTrue(any('invalid market price' in e for e in verify.validate()))
    def test_missing_variant(self):
        card=self.card()
        card['prints']=[]
        self.write(card)
        self.assertTrue(any('missing print variants' in e for e in verify.validate()))
    def test_empty_index(self):
        (self.root/'index.json').write_text('[]')
        self.assertTrue(verify.validate())
    def test_duplicate_product(self):
        card=self.card()
        (self.root/'index.json').write_text(json.dumps([{'id':'test-set'}]))
        (self.root/'test-set.json').write_text(json.dumps({'id':'test-set','cards':[card,card]}))
        self.assertTrue(any('duplicate' in e for e in verify.validate()))
if __name__=='__main__':
    unittest.main()
