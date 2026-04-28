import unittest
import os
import sys

# Шлях до папки з логікою
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic.rsa import RSA


class TestRSAProfessional(unittest.TestCase):
    def setUp(self):
        self.crypto = RSA(bit_length=2048)
        self.priv, self.pub = self.crypto.generate_keys()

    # Тест 1: Генерація ключів
    def test_key_properties(self):
        self.assertEqual(self.priv.key_size, 2048)
        self.assertTrue(hasattr(self.pub, "encrypt"))

    # Тест 2: Стандартне шифрування (Короткий текст)
    def test_small_string(self):
        msg = b"Slytherin Ambition"
        encrypted = self.crypto.encrypt_data(self.pub, msg)
        decrypted = self.crypto.decrypt_data(self.priv, encrypted)
        self.assertEqual(msg, decrypted)

    # Тест 3: Тот самий "Чанкінг" (Великі дані)
    def test_large_chunking(self):
        # Генеруємо дані на 2 КБ (це багато блоків по 190 байт)
        large_data = os.urandom(2048)
        encrypted = self.crypto.encrypt_data(self.pub, large_data)
        # Перевіряємо, що шифротекст став більшим за оригінал (це норма для RSA)
        self.assertGreater(len(encrypted), len(large_data))
        decrypted = self.crypto.decrypt_data(self.priv, encrypted)
        self.assertEqual(large_data, decrypted)

    # Тест 4: Збереження та читання PEM (Файлова система)
    def test_pem_serialization(self):
        self.crypto.save_keys(self.priv, self.pub, prefix="temp_test")

        loaded_priv = self.crypto.load_private_key("temp_test_private.pem")
        loaded_pub = self.crypto.load_public_key("temp_test_public.pem")

        # Перевіряємо, що завантажений ключ працює
        msg = b"File Test"
        enc = self.crypto.encrypt_data(loaded_pub, msg)
        self.assertEqual(msg, self.crypto.decrypt_data(loaded_priv, enc))

        # Чистимо сміття
        os.remove("temp_test_private.pem")
        os.remove("temp_test_public.pem")

    # Тест 5: Цілісність (Пошкодження шифротексту)
    def test_integrity_fail(self):
        msg = b"Secure Data"
        encrypted = bytearray(self.crypto.encrypt_data(self.pub, msg))
        # Псуємо один байт у зашифрованих даних
        encrypted[50] = (encrypted[50] + 1) % 256

        # Дешифрування має впасти через неправильний падінг (OAEP перевіряє це)
        with self.assertRaises(Exception):
            self.crypto.decrypt_data(self.priv, bytes(encrypted))

    # Тест 6: Пусті дані
    def test_empty_bytes(self):
        msg = b""
        encrypted = self.crypto.encrypt_data(self.pub, msg)
        self.assertEqual(b"", self.crypto.decrypt_data(self.priv, encrypted))


if __name__ == '__main__':
    unittest.main()