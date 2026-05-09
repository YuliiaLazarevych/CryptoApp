import math
import struct


class MD5:
    def __init__(self):
        self.init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

        self.T = [int(4294967296 * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]

        self.S = [
            7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
            5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
            4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
            6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
        ]

    @staticmethod
    def _left_rotate(x, amount):
        return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

    def hash_string(self, message: str) -> str:
        return self.hash_bytes(message.encode('utf-8'))

    def hash_bytes(self, data: bytes) -> str:
        orig_len_bits = (len(data) * 8) & 0xFFFFFFFFFFFFFFFF
        data += b'\x80'
        while (len(data) * 8) % 512 != 448:
            data += b'\x00'
        data += struct.pack('<Q', orig_len_bits)

        a, b, c, d = self.init_values

        for i in range(0, len(data), 64):
            block = data[i:i + 64]
            X = list(struct.unpack('<16I', block))
            aa, bb, cc, dd = a, b, c, d

            for j in range(64):
                if 0 <= j <= 15:
                    f = (b & c) | ((~b) & d)
                    g = j
                elif 16 <= j <= 31:
                    f = (d & b) | ((~d) & c)
                    g = (5 * j + 1) % 16
                elif 32 <= j <= 47:
                    f = b ^ c ^ d
                    g = (3 * j + 5) % 16
                else:
                    f = c ^ (b | (~d))
                    g = (7 * j) % 16

                temp = (a + f + self.T[j] + X[g]) & 0xFFFFFFFF
                a = d
                d = c
                c = b
                b = (b + self._left_rotate(temp, self.S[j])) & 0xFFFFFFFF

            a = (a + aa) & 0xFFFFFFFF
            b = (b + bb) & 0xFFFFFFFF
            c = (c + cc) & 0xFFFFFFFF
            d = (d + dd) & 0xFFFFFFFF

        return ''.join(f'{x:02x}' for x in struct.pack('<4I', a, b, c, d)).upper()

    def check_file_integrity(self, filepath: str, expected_hash: str) -> bool:
        with open(filepath, 'rb') as f:
            file_data = f.read()
        actual_hash = self.hash_bytes(file_data)
        return actual_hash == expected_hash.upper()