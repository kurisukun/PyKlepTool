import tkinter as tk
import secrets
from base64 import b64encode
from setup_attacks.rsa.setup_rsa import encode_message

def enable_element(elements):
    for el in elements:
        el["state"] = "normal"


# Better encoding function thanks to https://stackoverflow.com/a/12626870/13329098
def numfy(s):
    number = 0
    for e in [ord(c) for c in s]:
        number = (number * 0x110000) + e
    return number

# Better decoding function thanks to https://stackoverflow.com/a/12626870/13329098
def denumfy(number):
    l = []
    while(number != 0):
        l.append(chr(number % 0x110000))
        number = number // 0x110000
    return ''.join(reversed(l))


def random_key():
    key = b64encode(secrets.token_bytes(16)).decode('utf-8')
    key = encode_message(key)
    return key

def change_value_elements(el, value):
    el.delete(1.0, tk.END)
    el.insert(1.0, value)