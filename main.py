import argparse
import json


def preprocess(text):
    """
    Check that format and character set are valid before cracking
    :param text: Cipher-text as a string.
    :return: The properly formatted cipher-text.
    """
    # Remove all whitespace
    text = "".join(text.split())

    # Check that text is only alphabet characters
    if not text.isalpha():
        raise ValueError("Cipher-text must only contain English alphabet characters.")

    # Make everything lower-case for consistency
    text = text.lower()

    return text


def decrypt(cipher_text, freq):
    """
    Main algorithm flow for decryption.
    :param cipher_text: The cipher-text as a string. Assumes cipher-text has went through preprocess.
    :param freq: Dict containing the letter frequency distribution.
    :return: TODO!
    """

    print(cipher_text)
    print(freq)

    # TODO: you are here!!
    # Find the occurrence for each letter
    ct_freq = {}
    for letter in cipher_text:
        if not ct_freq[letter]:
            ct_freq[letter] = 1
        else:
            ct_freq[letter] = ct_freq[letter] + 1

    print ct_freq


if __name__ == "__main__":
    # Parse Args
    parser = argparse.ArgumentParser()
    parser.add_argument('cipher_file', metavar='C', type=str, help="Text file containing the cipher-text.")
    parser.add_argument('--freq', dest='freq_json', type=str, default="frequencies/us_english.json",
                        help="Optional: json file containing a letter frequency distribution.")
    args = parser.parse_args()

    # Prepare user inputs for decryption
    with open(args.cipher_file, 'r') as c_handle:
        with open(args.freq_json, 'r') as f_handle:
            ct = preprocess(c_handle.read())
            f = json.loads(f_handle.read())

    decrypt(ct, f)
