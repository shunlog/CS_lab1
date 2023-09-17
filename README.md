# CS lab 1: Caesar cipher

## Usage

```
$ ./caesar.py -h 
usage: Caesar cipher [-h] [--decrypt] -k NUM [-k2 WORD] [--verbosity {0,1}] text

Encrypt or decrypt a text using the Caesar cipher

positional arguments:
  text

options:
  -h, --help            show this help message and exit
  --decrypt, -d         decrypt if specified; default is encryption
  -k NUM                the shift amount
  -k2 WORD              string that defines the permutation of the alphabet
  --verbosity {0,1}, -v {0,1}
                        verbosity level, 0 for WARNING (default), 1 for INFO
```
