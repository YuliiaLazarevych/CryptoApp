import unittest
from logic.md5 import MD5


class TestMD5(unittest.TestCase):
    def setUp(self):
        self.md5 = MD5()

    def test_rfc_vectors(self):
        # тестові вектори з методички
        test_cases = {
            "": "D41D8CD98F00B204E9800998ECF8427E",
            "a": "0CC175B9C0F1B6A831C399E269772661",
            "abc": "900150983CD24FB0D6963F7D28E17F72",
            "message digest": "F96B697D7CB7938D525A2F31AAF161D0",
            "abcdefghijklmnopqrstuvwxyz": "C3FCD3D76192E4007DFB496CCA67E13B",
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789": "D174AB98D277D9F5A5611C2C9F419D9F",
            "12345678901234567890123456789012345678901234567890123456789012345678901234567890": "57EDF4A22BE3C955AC49DA2E2107B67A"
        }

        for msg, expected in test_cases.items():
            with self.subTest(msg=msg):
                self.assertEqual(self.md5.hash_string(msg), expected)

if __name__ == '__main__':
    unittest.main()
