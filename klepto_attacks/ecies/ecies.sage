import hashlib
import hmac
from base64 import b64encode
from base64 import b64decode
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os


#Parameters come from http://www.secg.org/sec2-v2.pdf
### EC Constants
#Domain
p256 = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF

#Curve parameters for the curve equation: y^2 = x^3 + a256*x +b256
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B

#Base point definition
Gx = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
Gy = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5


#Curve order
n = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551

FF = GF(p256)

# Define a curve over that field with specified Weierstrass a and b parameters
E = EllipticCurve(FF, [a,b])
E.set_order(n)

G = E(FF(Gx), FF(Gy))


def H(m):
	return hashlib.sha512(m).digest()

def ecies_key_gen():
	kpriv = ZZ.random_element(0,n)
	kpub = G * kpriv
	return (kpriv, kpub)

def KEM_Rg():
	return ZZ.random_element(1,n)

def KEM_Kg(psk, r):
	return H(str((psk * r).xy()).encode('utf-8'))

def KEM_Cg(r):
	return r*G


def KEM_Kd(dk, C):
	return H(str((dk * C).xy()).encode('utf-8'))

def ASA_Gen():
	ssk = ZZ.random_element(0,n)
	psk = G * ssk
	return (psk, ssk)


def ASA_Enc(pk, psk, tau):
	t = None
	r = None
	if tau == 0:
		r = KEM_Rg()
	else:
		t = KEM_Kg(psk, tau)
		r = int.from_bytes(H(t), byteorder='little')

	Ki = KEM_Kg(pk, r)
	Ci = KEM_Cg(r)
	tau = r
	return (Ki, Ci, tau)


def ASA_Rec(pk, ssk, Ci, Ci_prev):
	t = KEM_Kd(ssk, Ci_prev)
	r = int.from_bytes(H(t), byteorder='little')
	Ki = KEM_Kg(pk, r)
	return Ki

def DEM_Encrypt(keys, m):
	(kE, kM) = (keys[32:],keys[:32])
	nonce = get_random_bytes(16)
	cipher = AES.new(kE, AES.MODE_SIV, nonce=nonce) 
	n = b64encode(cipher.nonce).decode('utf-8')
	c, tag = cipher.encrypt_and_digest(m)
	return (c, tag, n)

def asa_decrypt(sk, c, tag, n):
	(R, ciphertext) = c
	keys = H(str((sk * R).xy()).encode('utf-8'))
	(kE, kM) = (keys[32:], keys[:32])
	n = b64decode(n)
	aes = AES.new(kE, AES.MODE_SIV, nonce=n)
	return aes.decrypt_and_verify(ciphertext, tag)

def asa_decrypt_broken(keys, ciphertext, tag, n):
	(kE, kM) = (keys[32:], keys[:32])
	n = b64decode(n)
	aes = AES.new(kE, AES.MODE_SIV, nonce=n)
	return aes.decrypt_and_verify(ciphertext, tag)