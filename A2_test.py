import pytest

import A2 as module

def test_isprime():
    prime_numbers = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    for prime_number in prime_numbers:
        assert module.isprime_naive(prime_number)
        assert module.isprime_miller_rabin(prime_number)
    non_prime_numbers = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 60, 62, 63, 64, 65, 66, 68, 69, 70, 72, 74, 75, 76, 77, 78, 80, 81, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 98, 99]
    for non_prime_number in non_prime_numbers:
        assert not module.isprime_naive(non_prime_number)
        assert not module.isprime_miller_rabin(non_prime_number)

def test_modular_exponentiation():
    assert module.fast_modular_exponentiation(2,10,7) == 2
    assert module.fast_modular_exponentiation(5,7,11) == 3
    assert module.fast_modular_exponentiation(3,20,17) == 13
    assert module.fast_modular_exponentiation(2,64,13) == 3
    assert module.fast_modular_exponentiation(17,3,5) == 3

def test_modular_inverse():
    assert module.modular_inverse(7,10) == 3
    assert module.modular_inverse(11,5) == 1
    assert module.modular_inverse(20,17) == 6
    assert module.modular_inverse(64,13) == 12
    assert module.modular_inverse(3,5) == 2

def test_encryption_RSA():
    p, q, e, M = 17, 11, 7, 88
    n = p*q
    assert module.encryption_RSA(M,[e,n]) == 11

def test_decryption_RSA():
    p, q, d, C = 17, 11, 23, 11
    n = p*q
    assert module.decryption_RSA(C,[d,n]) == 88