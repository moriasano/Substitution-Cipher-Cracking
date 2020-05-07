# Substitution Cipher Cracking
## Overview:
Final project for JHU Cryptography. This code cracks substitution ciphers using a hill-climbing approach. A random key
is generated. On each round, two key values are swapped and a language "fitness" score is determined. 

## Prerequisites:  
* Python 3+
* Cipher-text as a text file
## Usage  
Simple Usage for English language plain-texts
> python3 substitution_crack.py /path/to/cipher_text.txt

You can also provide (large) sample text for custom language fitness
> python3 substitution_crack.py /path/to/cipher_text.txt --training /path/to/training.txt

## Citations
Language Fitness - http://practicalcryptography.com/cryptanalysis/text-characterisation/quadgrams/
Training Text - https://www.gutenberg.org/files/11/11.txt