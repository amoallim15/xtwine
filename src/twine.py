import random
import string
import binascii
from math import ceil
from .algo import _key_schedule_80, _key_schedule_128, _encrypt, _decrypt


class Twine:
    key_space = [
        string.ascii_lowercase,
        string.ascii_uppercase,
        string.digits,
        # string.punctuation,
    ]

    def __init__(self, key=None, key_size=0x50):
        if type(key_size) == str:
            key_size = int(key_size, 0)
        if key_size not in [0x50, 0x80]:
            raise ValueError(
                f"the given key bit length of: {key_size} is not supported"
            )

        if not key:
            key = self.__generate_key(key_size)

        if self.__is_key_valid(key):
            self.key = key
        else:
            raise ValueError(f"The given key: {key} is not valid")

    @property
    def key_size(self):
        return len(str(self.key).encode("utf-8"))

    def __is_key_valid(self, key):
        kl = len(str(key).encode("utf-8"))
        if kl != 0x0A and kl != 0x10:
            return False
        return True

    def __generate_key(self, key_size):
        space = "".join(self.key_space)
        if key_size == 0x50:
            return "".join(random.choice(space) for i in range(0x0A))
        elif key_size == 0x80:
            return "".join(random.choice(space) for i in range(0x10))

    def __generate_RK(self):
        if self.key_size == 0x50:
            return _key_schedule_80(int(self.key.encode("utf-8").hex(), 16))
        else:
            return _key_schedule_128(int(self.key.encode("utf-8").hex(), 16))

    def __iterblocks(self, blocks):
        for i in range(ceil(len(blocks) / 16)):
            if i * 16 + 16 > len(blocks):
                yield blocks[i * 16 : len(blocks)]
            else:
                yield blocks[i * 16 : i * 16 + 16]

    def encrypt(self, plaintext):
        _c = ""
        plaintext = plaintext.encode("utf-8").hex()
        RK = self.__generate_RK()
        for block in self.__iterblocks(plaintext):
            cblock = hex(_encrypt(int(block, 16), RK))[2:]
            _c += cblock
        return _c

    def decrypt(self, ciphertext):
        _t = ""
        RK = self.__generate_RK()
        for block in self.__iterblocks(ciphertext):
            tblock = binascii.unhexlify(hex(_decrypt(int(block, 16), RK))[2:]).decode(
                "utf-8"
            )
            _t += tblock
        return _t
