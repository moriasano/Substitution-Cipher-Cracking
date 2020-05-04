# Substitution Cipher Cracking
## Overview:
Final project for JHU Cryptography. This code cracks substitution ciphers using a hill-climbing approach. A random key
is generated. On each round on letter of the key is modified and a language "fitness" test is performed to determine if
the new key is more or less fit. This continues until the fitness score cannot be improved.
## Prerequisites:  
* Python 3+
* Cipher-text as a text file
## Usage  
Simple Usage for English language plain-texts
> python substitution_crack.py /path/to/cipher_text.txt

You can also provide (large) sample text for custom language fitness
> python substitution_crack.py /path/to/cipher_text.txt --training /path/to/training.txt

## Citations
Language Fitness - http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/
Training Text - https://www.gutenberg.org/files/11/11.txt