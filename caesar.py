#!/bin/env python3
import sys
from string import ascii_uppercase as ABC, ascii_lowercase as abc
import argparse
from icecream import ic
from typing import Sequence
import logging


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

    logging.info('permuted_alphabet = {}'.format(abcp))


    return caesar(s, k, decrypt, abcp)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Caesar cipher',
        description='Encrypt or decrypt a text using the Caesar cipher')

    parser.add_argument('--decrypt', '-d', action='store_true',
                        help="decrypt if specified; default is encryption")
    parser.add_argument('-k', type=int, required=True, metavar="NUM",
                        help="the shift amount")
    parser.add_argument('-k2', default='', metavar="WORD",
                        help="string that defines the permutation of the alphabet")
    parser.add_argument('--verbosity', '-v', type=int, choices=[0, 1], default=0,
                        help="verbosity level, 0 for WARNING (default), 1 for INFO")
    parser.add_argument('text')

    r = parser.parse_args()
    s, k, k2, decrypt = r.text, r.k, r.k2, r.decrypt

    level = (logging.WARNING, logging.INFO)[r.verbosity]
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=level)


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
