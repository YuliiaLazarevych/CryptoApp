from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend

class DSALogic:
    def __init__(self, key_size: int = 1024):
        self._key_size = key_size
        self._backend = default_backend()

    def generate_keys(self):
        priv = dsa.generate_private_key(key_size=self._key_size, backend=self._backend)
        return priv, priv.public_key()

    def save_keys(self, priv_key, pub_key, prefix="dsa"):
        with open(f"{prefix}_private.pem", "wb") as f:
            f.write(priv_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open(f"{prefix}_public.pem", "wb") as f:
            f.write(pub_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def load_private_key(self, path):
        with open(path, "rb") as f:
            return serialization.load_pem_private_key(f.read(), None, self._backend)

    def load_public_key(self, path):
        with open(path, "rb") as f:
            return serialization.load_pem_public_key(f.read(), self._backend)

    def sign_data(self, priv_key, data: bytes) -> bytes:
        return priv_key.sign(data, hashes.SHA1())

    def verify_signature(self, pub_key, data: bytes, signature: bytes) -> bool:
        try:
            pub_key.verify(signature, data, hashes.SHA1())
            return True
        except InvalidSignature:
            return False