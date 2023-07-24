"""
Algorithms relating to strings
"""


def levenshtein_distance(string1: str, string2: str) -> int:
    """
    Takes two strings as input and returns their Levenshtein distance
    https://en.wikipedia.org/wiki/Levenshtein_distance
    """
    s = string1.lower()
    t = string2.lower()
    width = len(s) + 1
    height = len(t) + 1
    sizeOfMatrix = width * height
    d = [0] * sizeOfMatrix
    for j in range(width):
        d[j] = j
    for j in range(height):
        d[j * width] = j

    for y in range(1, height):
        for x in range(1, width):
            substitutionCost = s[x - 1] != t[y - 1]
            d[x + y * width] = min(
                d[x - 1 + y * width] + 1,  # deletion
                d[x + (y - 1) * width] + 1,  # insertion
                d[x - 1 + (y - 1) * width] + substitutionCost,  # substitution
            )

    return d[sizeOfMatrix - 1]


def hamming_encode(bitstring: str) -> str:
    """
    Input a bitstring and return its Hamming encoding
    https://en.wikipedia.org/wiki/Hamming_code
    """
    encode_bits = [int(x) for x in bitstring]
    i = 1
    while i - 1 < len(encode_bits):
        encode_bits.insert(i - 1, 0)
        i *= 2
    j = 1
    while j < i:
        encode_bits[j - 1] = (
            sum(x for k, x in enumerate(encode_bits) if j & (k + 1)) & 1
        )
        j *= 2
    return "".join(str(x) for x in encode_bits)


def hamming_decode(bitstring: str) -> str:
    """
    Input a Hamming-encoded bitstring and return decoded bitstring
    https://en.wikipedia.org/wiki/Hamming_code
    """
    decode_bits = [int(x) for x in bitstring]
    n = len(decode_bits)
    i = 1
    error_index = 0
    while i - 1 < n:
        check_sum = sum(x for k, x in enumerate(decode_bits) if i & (k + 1)) & 1
        error_index += check_sum * i
        i *= 2
    if error_index:
        decode_bits[error_index - 1] = 1 - decode_bits[error_index - 1]
    while i > 1:
        i //= 2
        decode_bits.pop(i - 1)
    return "".join(str(x) for x in decode_bits)


if __name__ == "__main__":
    # Tests
    print(levenshtein_distance("plain", "plane"))
    print(levenshtein_distance("flatterning", "acorn"))
    print(hamming_encode("111101"))
    print(hamming_encode("01011111"))
    print(hamming_decode("010100111"))
    print(hamming_decode("1001001101"))
