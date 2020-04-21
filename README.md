# Substitution Cipher Cracking
## Prerequisites:  
* Python 2.7+ (has not been tested with 3.x)  
* Cipher-text as a text file
## Usage  
From command line:
> python main.py cipher_text.txt

You can decrypt using a different letter frequency distribution; given as a json file:
> --freq /path/to/frequency.json

## Citations
Monograms - https://gist.github.com/evilpacket/5973230
Digraphs - http://pi.math.cornell.edu/~mec/2003-2004/cryptography/subs/digraphs.html
Trigraphs - http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/english-letter-frequencies/