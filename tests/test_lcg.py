import unittest
from logic.lcg import LCGGenerator

class TestLCG(unittest.TestCase):
    def setUp(self):
        self.gen = LCGGenerator()

    def test_gcd(self):
        self.assertEqual(self.gen.gcd(48, 18), 6)
        self.assertEqual(self.gen.gcd(17, 13), 1)

    def test_sequence_start(self):
        seq = self.gen.generate_sequence(1)
        self.assertEqual(seq[0], 221239)

    def test_sequence_length(self):
        n = 10
        seq = self.gen.generate_sequence(n)
        self.assertEqual(len(seq), n)

    def test_pi_estimation(self):
        pi_val = self.gen.estimate_pi(100, mode="lcg")
        self.assertIsInstance(pi_val, float)
        self.assertGreater(pi_val, 0)

if __name__ == "__main__":
    unittest.main()