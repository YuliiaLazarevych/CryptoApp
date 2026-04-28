from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from typing import Tuple, Generator


class RSA:
    def __init__(self, bit_length: int = 2048):
        self._key_size = bit_length
        self._backend = default_backend()
        self._hash_func = hashes.SHA256()

        self._padding_config = padding.OAEP(
            mgf=padding.MGF1(algorithm=self._hash_func),
            algorithm=self._hash_func,
            label=None
        )

        self.max_input_block = (bit_length // 8) - 2 * self._hash_func.digest_size - 2
        self.output_block_size = bit_length // 8

    def generate_key_pair(self) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        priv = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self._key_size,
            backend=self._backend
        )
        return priv, priv.public_key()

    def export_keys(self, priv_key, pub_key, base_name: str = "rsa_key"):
        with open(f"{base_name}_private.pem", "wb") as f:
            f.write(priv_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open(f"{base_name}_public.pem", "wb") as f:
            f.write(pub_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def _get_data_chunks(self, data: bytes, chunk_size: int) -> Generator[bytes, None, None]:
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]

    def process_encryption(self, key, raw_data: bytes) -> bytes:
        encrypted_buffer = []
        for chunk in self._get_data_chunks(raw_data, self.max_input_block):
            encrypted_buffer.append(key.encrypt(chunk, self._padding_config))
        return b"".join(encrypted_buffer)

    def process_decryption(self, key, cipher_data: bytes) -> bytes:
        decrypted_buffer = []
        for chunk in self._get_data_chunks(cipher_data, self.output_block_size):
            decrypted_buffer.append(key.decrypt(chunk, self._padding_config))
        return b"".join(decrypted_buffer)

    def generate_keys(self):
        return self.generate_key_pair()
    def encrypt_data(self, key, data):
        return self.process_encryption(key, data)
    def decrypt_data(self, key, data):
        return self.process_decryption(key, data)
    def save_keys(self, pr, pb, prefix="rsa"):
        self.export_keys(pr, pb, base_name=prefix)

    def load_private_key(self, p):
        with open(p, "rb") as f: return serialization.load_pem_private_key(f.read(), None, self._backend)

    def load_public_key(self, p):
        with open(p, "rb") as f: return serialization.load_pem_public_key(f.read(), self._backend)