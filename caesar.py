#!/bin/env python3
import sys
from string import ascii_uppercase as ABC, ascii_lowercase as abc
import argparse
from icecream import ic
from typing import Sequence

INFO = False

def print_info(m):
    if not INFO:
        return
    print('INFO: ', end='', file=sys.stderr)
    print(m, file=sys.stderr)


def caesar(s: Sequence, k: int, decrypt: bool = False, abcp: str = ABC) -> str:
    '''Encrypt/decrypt using the Caesar cipher.

    - s: the message, a sequence of characters in [A..Za..z ]
    - k: the key, an int such that `k % len(abcp) != 0`
    - decrypt: True if decrypting, False if encrypting

    Note: `s` will be converted to all uppercase and spaces are removed
    '''

    s = str(s).upper()
    s = ''.join(ch for ch in s if ch != ' ')
    n = len(abcp)
    k = k % n

    assert(all(ch in abcp for ch in s))
    assert(1 <= k <= n)

    trans = dict(zip(abcp, abcp[(k,n-k)[decrypt]:] + abcp[:(k,n-k)[decrypt]]))
    return ''.join(trans[L] for L in s.upper() if L in abcp)


def caesar_advanced(s: Sequence, k: int, k2: str = '', decrypt: bool = False) -> str:
    '''Like Caesar's, but support a second key which permutes the alphabet.'''

    def permute_alphabet(key: str):
        '''Permute the alphabet with a string key
        - key: string of uppercase letters'''
        abcp = ''
        for ch in key + ABC:
            if ch in abcp:
                continue
            abcp += ch
        return abcp

    k2 = str(k2).upper()
    abcp = permute_alphabet(k2)

    print_info('permuted_alphabet = {}'.format(abcp))

    return caesar(s, k, decrypt, abcp)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Caesar cipher',
        description='Encrypt or decrypt a text using the Caesar cipher')

    parser.add_argument('--decrypt', '-d', action='store_true')
    parser.add_argument('--key1', '-k1', type=int, required=True)
    parser.add_argument('--key2', '-k2', default='')
    parser.add_argument('--info', '-i', action='store_true')
    parser.add_argument('text')

    r = parser.parse_args()
    s, k, k2, decrypt, INFO = r.text, r.key1, r.key2, r.decrypt, r.info

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

    encrypted = caesar_advanced(s, k, k2, decrypt)
    print(encrypted)
