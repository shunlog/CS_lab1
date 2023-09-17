#!/bin/env python3
import sys
import argparse
import logging
from string import ascii_uppercase as ABC, ascii_lowercase as abc
from icecream import ic


def caesar(s: str, k: int, decrypt: bool = False, abc: str = ABC) -> str:
    '''Encrypt/decrypt using the Caesar cipher.

    - s: the message, a string of characters in [A..Za..z ]
    - k: the key, an int such that `k % len(abc) != 0`
    - decrypt: True if decrypting, False if encrypting

    Note: `s` will be converted to all uppercase and spaces are removed
    '''

    old_s = s
    s = s.upper()
    if old_s != s:
        logging.info("The input text has been converted to uppercase.")

    n = len(abc)
    k = k % n # shift

    if not all(ch in abc for ch in s):
        logging.info("Some characters are not in the alphabet and will be ignored.")

    assert 1 <= k <= n

    if decrypt:
        k = n - k

    trans = dict(zip(abc, abc[k:] + abc[:k]))
    logging.debug(f"trans = {trans}")
    return ''.join(trans[L] for L in s if L in abc)


def caesar_advanced(s: str, k: int, k2: str = '', decrypt: bool = False) -> str:
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

    if k2:
        k2 = str(k2).upper()
        abcp = permute_alphabet(k2)
        logging.debug('permuted_alphabet = {}'.format(abcp))
        return caesar(s, k, decrypt, abcp)
    else:
        return caesar(s, k, decrypt)


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
    parser.add_argument('--verbosity', '-v', type=int, choices=[0, 1, 2], default=0,
                        help="verbosity level, 0 for WARNING (default), 1 for INFO, 2 for DEBUG")
    parser.add_argument('text')

    r = parser.parse_args()
    s, k, k2, decrypt = r.text, r.k, r.k2, r.decrypt

    level = (logging.WARNING, logging.INFO, logging.DEBUG)[r.verbosity]
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=level)

    valid_chars = (abc + ABC + ' ')
    if not all(ch in valid_chars for ch in s):
        parser.error("The input text can contain only ASCII letters and spaces.")

    k = k % len(abc)
    if k == 0:
        parser.error("The key can't be 0 or a multiple of the alphabet length.")

    valid_chars = abc + ABC
    if not all(ch in valid_chars for ch in k2):
        parser.error("The second key can contain only ASCII letters and spaces.")

    print(caesar_advanced(s, k, k2, decrypt))
