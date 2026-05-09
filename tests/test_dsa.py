import unittest
import os
import tempfile
from logic.dsa import DSALogic
from cryptography.exceptions import InvalidSignature


class TestDSAAdvanced(unittest.TestCase):
    def setUp(self):
        self.logic = DSALogic(key_size=1024)
        self.priv, self.pub = self.logic.generate_keys()

    def test_standard_flow(self):
        data = b"Lviv Polytechnic National University - AI Department"
        sig = self.logic.sign_data(self.priv, data)
        self.assertTrue(self.logic.verify_signature(self.pub, data, sig))

    def test_data_integrity(self):
        data = b"Original data"
        sig = self.logic.sign_data(self.priv, data)
        self.assertFalse(self.logic.verify_signature(self.pub, b"Modified data", sig))

    def test_empty_data(self):
        data = b""
        sig = self.logic.sign_data(self.priv, data)
        self.assertTrue(self.logic.verify_signature(self.pub, data, sig))

    def test_corrupted_signature(self):
        data = b"Secure transaction"
        sig = bytearray(self.logic.sign_data(self.priv, data))
        sig[0] = (sig[0] + 1) % 256
        self.assertFalse(self.logic.verify_signature(self.pub, data, bytes(sig)))

    def test_keys_persistence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            prefix = os.path.join(tmpdir, "test_dsa")
            self.logic.save_keys(self.priv, self.pub, prefix=prefix)

            loaded_priv = self.logic.load_private_key(f"{prefix}_private.pem")
            loaded_pub = self.logic.load_public_key(f"{prefix}_public.pem")

            data = b"Persistence test"
            sig = loaded_priv.sign(data, self.logic.sign_data.__globals__['hashes'].SHA1())
            loaded_pub.verify(sig, data, self.logic.sign_data.__globals__['hashes'].SHA1())

    def test_large_data(self):
        data = os.urandom(1024 * 1024)
        sig = self.logic.sign_data(self.priv, data)
        self.assertTrue(self.logic.verify_signature(self.pub, data, sig))