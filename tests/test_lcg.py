import unittest
from logic.lcg import LCGGenerator

class TestLCG(unittest.TestCase):
    def setUp(self):
        self.gen = LCGGenerator()

    # перший тест: перевірка НСД для алгоритму Евкліда
    def test_gcd(self):
        # НСД(48, 18) має бути 6
        self.assertEqual(self.gen.gcd(48, 18), 6)
        # перевіряємо взаємно прості числа, має вийти 1
        self.assertEqual(self.gen.gcd(17, 13), 1)

    # другий тест: перевірка першого числа послідовності
    def test_sequence_start(self):
        # (216 * 1024 + 55) % 524287 = 221239
        seq = self.gen.generate_sequence(1)
        self.assertEqual(seq[0], 221239)

    # третій тест: перевірка довжини списку
    def test_sequence_length(self):
        # вводимо 10 чисел, і має вийти список із 10 елементів
        n = 10
        seq = self.gen.generate_sequence(n)
        self.assertEqual(len(seq), n)

    # четвертий тест: перевірка оцінки пі
    def test_pi_estimation(self):
        # оцінка має бути типу float і бути більшою за 0
        pi_val = self.gen.estimate_pi(100, mode="lcg")
        self.assertIsInstance(pi_val, float)
        self.assertGreater(pi_val, 0)

if __name__ == "__main__":
    unittest.main()