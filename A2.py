import random
import string
import math
import matplotlib.pyplot as plt

def isprime_naive(n:int) -> bool:
    """
    Indentify if an integer is prime or not with a naive approach.

    Args:
        n: Integer studied.

    Returns:
        True if the integer is prime else False.
    """
    if n <= 1:
        return False
    for i in range(2,int(math.sqrt(n))+1):
        if n % i == 0:
            return False
    return True


def isprime_miller_rabin(n, k=5):
    """
    Indentify if an integer is prime or not with a probalistic test repeated k times. Bigger k is, more accurate the prediction is.
    Reference of the code:  

    Args:
        n: Integer studied.
        k: Number of test done

    Returns:
        True if the integer is prime else False. Notice that it's a probalistic result.
    """
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def gcd(a:int, b:int) -> int:
    """
    Calculate highest common factor with a >= b.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        Highest common factor.
    """
    while b:
        a, b = b, a%b
    return abs(a)

def fast_modular_exponentiation(a, b, n):
    """
    Fast modular exponentiation to compute fastly modular exponentiation for large numbers. Complexity of this algorithm is log(b) multiplications instead of b multiplications is the naive one.
    Formula: a**b mod n

    Args:
        a: Integer according to formula.
        b: Integer according to formula.
        n: Integer according to formula.

    Returns:
        Result of a**b mod n.
    """
    result, base = 1, a % n

    while b > 0:
        # If the least significant bit of b is 1, multiply result by base modulo n
        if b % 2 == 1:
            result = (result * base) % n

        # Square the base and halve b (right shift)
        base = (base * base) % n
        b //= 2

    return result

def modular_inverse(a:int, m:int) -> int:
    """
    Calculate the modular inverse of a modulo m using the extended Euclidean algorithm.

    Args:
        a: Integer
        m: Integer
    
    Returns:
        Modular inverse of a modulo m.
    """
    if m == 1:
        return 0

    m0, x0, x1 = m, 0, 1

    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0

    if x1 < 0:
        x1 += m0

    return x1

def generate_keys(length:int) -> ([int,int],[int,int]):
    """Generating RSA key pairs for public and private keys.

    Args:
        length: Number of digits wanted for the prime numbers p and q.

    Returns:
        Public and private keys with respectively [e,n] and [d,n].
    """
    digits, p, q = string.digits, 0, 0

    while not isprime_miller_rabin(p):
        # Randomly choose digit from digits for the given length of the prime number
        p = int(''.join(random.choice(digits) for i in range(length)))

    while not isprime_miller_rabin(q):
        q = int(''.join(random.choice(digits) for i in range(length)))

    n = p*q
    phi_n = (p-1)*(q-1)
    e = 65537
    assert gcd(phi_n,e) == 1
    d = modular_inverse(e, phi_n)
    
    return [e, n], [d, n]

def encryption_RSA(plaintext: int, public_key:[int,int]) -> int:
    """Implementation of RSA encryption.

    Args:
        plaintext: Integer which will be encrypted.
        public_key: Array of two integers, respectively e and n, needed for the encryption process.

    Returns:
        Ciphertext which is an integer.
    """
    e, n = public_key
    cipher = fast_modular_exponentiation(plaintext,e,n)
    return cipher

def decryption_RSA(cipher:int, private_key:[int,int]) -> int:
    """Implementation of RSA decryption.

    Args:
        ciphertext: Integer which will be decrypted.
        private_key: Array of two integers, respectively d and n, needed for the decryption process.

    Returns:
        Original plaintext which is an integer.
    """
    d, n = private_key
    original_plaintext = fast_modular_exponentiation(cipher,d,n)
    return original_plaintext

if __name__ == "__main__":
    
    print("KEY GENERATION")
    length = 300
    print("This task is carried out by the bank's departments. Public key is sent to Alice to manage her encryption.")
    public_key, private_key = generate_keys(length)
    print("Generation completed.")

    print("Number of digits for p and q: ", length)
    bank_id = 11820329401
    print("In our use case, the bank id of Alice need to be protected thanks to RSA encryption.")
    print("Alice's bank id: ", bank_id)

    bank_id_encrypted = encryption_RSA(bank_id, public_key)
    print("Encryption of Alice's bank id thanks to the public key: ", bank_id_encrypted)
    print("Now that the data is encrypted, Alice's bank id can be send to the bank service.")

    bank_id_decrypted = decryption_RSA(bank_id_encrypted, private_key)
    print("Once received, bank's departement decrypter the cyphertext and get Alice's bank id.")
    print(bank_id_decrypted)
    
    print("Trade off between security and speed")
    lengths = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    delays = [0.1, 0.6, 1.1, 4.1, 10.1, 38.6, 52.6, 77.5, 109.9, 153.2]
    plt.figure(figsize=(9, 6))
    plt.bar(lengths, delays, color='skyblue', width=40)
    plt.xlabel('P and q length (bits)')
    plt.ylabel('Processing time (seconds)')
    for x, y in zip(lengths, delays):
        plt.text(x, y + 5, str(y), ha='center', va='bottom')
    plt.xticks(lengths) 
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add horizontal grid lines
    plt.show()
    

