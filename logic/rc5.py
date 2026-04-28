import struct
from logic.md5 import MD5
from logic.lcg import LCGGenerator

class RC5:
    def __init__(self, password_phrase: str, w=16, r=12, b=16):
        self.w = w
        self.r = r
        self.b = b
        self.mod = 2 ** w
        self.mask = self.mod - 1

        self.P = 0xB7E1
        self.Q = 0x9E37

        key = self._derive_key(password_phrase)
        self._expand_key(key)

    def _derive_key(self, password: str) -> bytes:
        md5 = MD5()
        h1 = bytes.fromhex(md5.hash_string(password))
        if self.b == 16:
            return h1
        elif self.b == 32:
            h2 = bytes.fromhex(md5.hash_bytes(h1))
            return h2 + h1
        return h1[:self.b]

    def _l_rot(self, val, n):
        n %= self.w
        return ((val << n) & self.mask) | (val >> (self.w - n))

    def _r_rot(self, val, n):
        n %= self.w
        return (val >> n) | ((val << (self.w - n)) & self.mask)

    def _expand_key(self, key):
        u = self.w // 8
        c = max(1, len(key) // u)
        L = [0] * c
        for i in range(len(key) - 1, -1, -1):
            L[i // u] = (L[i // u] << 8) + key[i]

        t = 2 * (self.r + 1)
        self.S = [0] * t
        self.S[0] = self.P
        for i in range(1, t):
            self.S[i] = (self.S[i - 1] + self.Q) & self.mask

        i = j = A = B = 0
        for _ in range(3 * max(c, t)):
            A = self.S[i] = self._l_rot((self.S[i] + A + B) & self.mask, 3)
            B = L[j] = self._l_rot((L[j] + A + B) & self.mask, A + B)
            i = (i + 1) % t
            j = (j + 1) % c

    def encrypt_block(self, data: bytes):
        A, B = struct.unpack('<HH', data)
        A = (A + self.S[0]) & self.mask
        B = (B + self.S[1]) & self.mask
        for i in range(1, self.r + 1):
            A = (self._l_rot(A ^ B, B) + self.S[2 * i]) & self.mask
            B = (self._l_rot(B ^ A, A) + self.S[2 * i + 1]) & self.mask
        return struct.pack('<HH', A, B)

    def decrypt_block(self, data: bytes):
        A, B = struct.unpack('<HH', data)
        for i in range(self.r, 0, -1):
            B = self._r_rot((B - self.S[2 * i + 1]) & self.mask, A) ^ A
            A = self._r_rot((A - self.S[2 * i]) & self.mask, B) ^ B
        B = (B - self.S[1]) & self.mask
        A = (A - self.S[0]) & self.mask
        return struct.pack('<HH', A, B)

    def process_cbc(self, data: bytes, iv: bytes, encrypt=True):
        if encrypt:
            pad = 4 - (len(data) % 4)
            data += bytes([pad] * pad)
            output = b""
            last_block = iv
            for i in range(0, len(data), 4):
                chunk = data[i:i+4]
                ready = bytes(x ^ y for x, y in zip(chunk, last_block))
                cipher_chunk = self.encrypt_block(ready)
                output += cipher_chunk
                last_block = cipher_chunk
            return output
        else:
            output = b""
            last_block = iv
            for i in range(0, len(data), 4):
                chunk = data[i:i+4]
                dec = self.decrypt_block(chunk)
                output += bytes(x ^ y for x, y in zip(dec, last_block))
                last_block = chunk
            return output[:-output[-1]]

    def encrypt_file(self, in_data: bytes):
        lcg = LCGGenerator()
        iv = struct.pack('<I', lcg.generate_sequence(1)[0] & 0xFFFFFFFF)[:4]
        return self.encrypt_block(iv) + self.process_cbc(in_data, iv, encrypt=True)

    def decrypt_file(self, data: bytes):
        iv = self.decrypt_block(data[:4])
        return self.process_cbc(data[4:], iv, encrypt=False)