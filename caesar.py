#!/bin/env python3
from string import ascii_uppercase as ABC, ascii_lowercase as abc
import argparse
from icecream import ic
from typing import Sequence

def caesar(s: Sequence, k: int, k2: str = '', decrypt: bool = False) -> str:
    '''Encrypt/decrypt using the Caesar cipher.

    - s: the message, a sequence of characters in [A..Za..z ]
    - k: the key, an int other than 0
    - k2: the second key used to permute the alphabet, a sequence of characters in [A..Za..z ]
    - decrypt: True if decrypting, False if encrypting

    Note: `s` will be converted to all uppercase and spaces are removed
    '''

    s = str(s).upper()
    s = ''.join(ch for ch in s if ch != ' ')
    k = k % 26
    k2 = str(k2).upper()
    abcp = permute_alphabet(k2)

    assert(all(ch in abcp for ch in s))
    assert(1 <= k <= 26)
    assert(abcp.isupper() and all(ch in ABC for ch in abcp))

    trans = dict(zip(abcp, abcp[(k,26-k)[decrypt]:] + abcp[:(k,26-k)[decrypt]]))
    return ''.join(trans[L] for L in s.upper() if L in abcp)


def permute_alphabet(key: str):
    '''Permute the alphabet with a string key
    - key: string of uppercase letters'''
    abcp = ''

    for ch in key + ABC:
        if ch in abcp:
            continue
        abcp += ch

    return abcp


def caesar_helper(s: str, k: int, k2: str = '', decrypt: bool = False):

    return caesar(s, k, k2, decrypt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Caesar cipher',
        description='Encrypt and decrypt a text using Caesar cipher')

    parser.add_argument('--decrypt', '-d', action='store_true')
    parser.add_argument('--key1', '-k1', type=int, required=True)
    parser.add_argument('--key2', '-k2', default='')
    parser.add_argument('text')

    r = parser.parse_args()
    s, k, k2, decrypt = r.text, r.key1, r.key2, r.decrypt

    try:
        assert(type(s) == str)
        valid_chars = (abc + ABC + ' ')
        assert(all(ch in valid_chars for ch in s))
    except AssertionError:
        parser.error("The string must contain only ASCII letters and spaces.")

    try:
        assert(type(k) == int)
        assert(k != 0)
    except AssertionError:
        parser.error("The key must be a non-zero integer.")

    try:
        assert(type(decrypt) == bool)
    except AssertionError:
        parser.error("The 'decrypt' parameter must be a boolean.")

    try:
        assert(type(k2) == str)
        valid_chars = abc + ABC
        assert(all(ch in valid_chars for ch in k2))
    except AssertionError as e:
        parser.error("The 'k2' parameter must be a string of lating characters.")

    encrypted = caesar(s, k, k2, decrypt)
    print(encrypted)
