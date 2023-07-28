"""
Basic algebraic algorithms
"""

import math


def sieve_of_eratosthenes(N: int) -> list:
    """
    Returns list of primes < N.
    Basic implementation using only standard library.
    """
    is_prime = [1] * N
    is_prime[0] = 0
    is_prime[1] = 0
    for j in range(4, N, 2):
        is_prime[j] = 0
    for i in range(3, math.isqrt(N) + 1, 2):
        if is_prime[i]:
            for j in range(i * i, N, 2 * i):
                is_prime[j] = 0
    return [p for p, b in enumerate(is_prime) if b]


def extended_euclidean_algorithm(a: int, b: int) -> int:
    """
    Returns (x, y, gcd) where a*x + b*y = gcd (the greatest common divisor of a and b).
    i.e. coefficients for Bezout's identity.
    """
    gcd, new_gcd = a, b
    x, new_x = 1, 0
    y, new_y = 0, 1

    while new_gcd:
        q = gcd // new_gcd
        gcd, new_gcd = new_gcd, gcd - q * new_gcd
        x, new_x = new_x, x - q * new_x
        y, new_y = new_y, y - q * new_y

    return (x, y, gcd)


if __name__ == "__main__":
    print(sieve_of_eratosthenes(30))
    print(extended_euclidean_algorithm(11, 5))
    print(extended_euclidean_algorithm(4, 14))
