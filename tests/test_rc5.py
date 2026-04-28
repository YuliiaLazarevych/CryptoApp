import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logic.rc5 import RC5

class TestRC5(unittest.TestCase):
    def setUp(self):
        self.password = "my_super_secret_password"
        self.iv = b"1234"
        self.cipher = RC5(self.password)

    def test_block_roundtrip(self):
        original = b"test"  # Рівно 4 байти
        encrypted = self.cipher.encrypt_block(original)
        decrypted = self.cipher.decrypt_block(encrypted)
        self.assertEqual(original, decrypted)

    def test_file_encryption_roundtrip(self):
        original_data = b"This is some secret data that needs encryption!"

        # Використовуємо методи encrypt_file / decrypt_file
        encrypted = self.cipher.encrypt_file(original_data)
        decrypted = self.cipher.decrypt_file(encrypted)

        self.assertEqual(original_data, decrypted)

    def test_padding_logic(self):
        short_data = b"123"
        encrypted = self.cipher.encrypt_file(short_data)

        self.assertEqual(len(encrypted), 8)

        decrypted = self.cipher.decrypt_file(encrypted)
        self.assertEqual(short_data, decrypted)


if __name__ == '__main__':
    unittest.main()