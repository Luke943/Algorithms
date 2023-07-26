"""
Ciphers to encode and decode messages
"""

import os
import string


def caesar(text: str, shift: int) -> str:
    """
    Returns encoded version of input text with Caesar cipher.
    To decode, use shift value as negative of the value used for encoding.
    """
    alphabets = (string.ascii_lowercase, string.ascii_uppercase, string.digits)
    shifted_alphabets = (a[shift % len(a) :] + a[: shift % len(a)] for a in alphabets)
    cipher_table = str.maketrans("".join(alphabets), "".join(shifted_alphabets))
    return text.translate(cipher_table)


def random_key(size: int) -> bytes:
    """
    Returns a stream of random bytes of length size.
    """
    return os.urandom(size)


def one_time_pad(message: bytes | str, key: bytes | str) -> bytes:
    """
    One-time pad encoding of text using xor operation.
    Accepts bytes or strings (assumes utf-8 encoding).
    To decode, use the same key on the encoded text.
    """
    if len(key) < len(message):
        raise ValueError("key must be at least as long as text")
    if type(message) == str:
        message = bytes(message, "utf-8")
    if type(key) == str:
        key = bytes(key, "utf-8")
    return bytes(t ^ k for t, k in zip(message, key))


if __name__ == "__main__":
    # Tests
    code = caesar("Hello world! 567", 51)
    decode = caesar(code, -51)
    print(code, decode)
    key = random_key(5)
    code2 = one_time_pad("HELLO", key)
    decode2 = one_time_pad(code2, key)
    print(code2, decode2)
