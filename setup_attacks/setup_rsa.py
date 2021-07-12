
# This file was *autogenerated* from the file rsa.sage
from sage.all import *   # import sage library

_sage_const_0 = 0; _sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_32 = Integer(32)
def encode_message(m):
    return int("".join(list(map(lambda c: str(ord(c)), list(m)))))

def rsa_encrypt(m, e, n) :
    c = power_mod (m, e, n)
    return c

def rsa_decrypt(c, d, n) :
    m = power_mod(c, d, n)
    return m

def setup_attacker_key_gen(size):
    P = _sage_const_0 
    Q = random_prime(_sage_const_2 **(size / _sage_const_2 ), lbound=_sage_const_2 **(size/_sage_const_2 -_sage_const_1))
    phi = _sage_const_0
    N = _sage_const_0
    E = _sage_const_0
    while True:
        P = random_prime(_sage_const_2 ** (size / _sage_const_2),lbound=_sage_const_2 ** (size / _sage_const_2 - _sage_const_1))
        E = ZZ.random_element(_sage_const_1, _sage_const_2 ** (size / _sage_const_2 - _sage_const_1))
        N = P * Q
        phi = (P - _sage_const_1) * (Q - _sage_const_1)
        if gcd(E, phi) == _sage_const_1 and _sage_const_1 < E and E < phi:
            break
    D = inverse_mod(E, phi)
    return (E, D, N)


def setup_victim_key_gen(size, E, N):
    p = _sage_const_0
    q = random_prime(_sage_const_2**(size / _sage_const_2),
                     lbound=_sage_const_2**(size / _sage_const_2 - _sage_const_1))
    phi = _sage_const_0
    n = _sage_const_0
    e = _sage_const_0
    while gcd(e, phi) != _sage_const_1:
        p = random_prime(_sage_const_2 ** (size / _sage_const_2),
                         lbound=_sage_const_2**(size / _sage_const_2 - _sage_const_1))
        n = p * q
        phi = (p - _sage_const_1) * (q - _sage_const_1)
        e = power_mod(p, E, N)
    d = inverse_mod(e, phi)
    return (e, d, n)


def rsa_setup_attack(c, D, N, e, n):
    p = power_mod(e, D, N)
    q = n / p
    phi = (p - _sage_const_1) * (q - _sage_const_1)
    d = inverse_mod(e, phi)
    return rsa_decrypt(c, d, n)
