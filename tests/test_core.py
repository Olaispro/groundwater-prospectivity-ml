import unittest
from src.model import generate
class TestSyntheticGenerator(unittest.TestCase):
 def test_reproducible(self):
  x,y=generate(30,seed=3); x2,y2=generate(30,seed=3); self.assertEqual(x.shape,(30,5)); self.assertEqual(y.shape,(30,)); self.assertTrue((x==x2).all()); self.assertTrue((y==y2).all())
