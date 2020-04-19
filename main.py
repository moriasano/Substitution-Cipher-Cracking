import argparse
import json

# Used whenever we need to map anything across the entire alphabet
LETTERS = {
    "a": None, "b": None, "c": None, "d": None, "e": None, "f": None, "g": None, "h": None, "i": None,
    "j": None, "k": None, "l": None, "m": None, "n": None, "o": None, "p": None, "q": None, "r": None,
    "s": None, "t": None, "u": None, "v": None, "w": None, "x": None, "y": None, "z": None
}


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


def substitute(ct, subs):
    """
    Perform substitutions on the cipher-text.
    :param ct: The cipher-text string.
    :param subs: Dict with mappings from cipher-text to plain-text letters.
    :return: The text with all the substitutions performed.
    """
    # Create a list of letters from string; for indexing
    pt = [letter for letter in ct]

    for orig, sub in subs.iteritems():
        i = 0
        for letter in ct:
            if letter == orig:
                pt[i] = sub
            i += 1

    pt = "".join(pt)
    return pt


def decrypt(cipher_text, freq):
    """
    Main algorithm flow for decryption.
    :param cipher_text: The cipher-text as a string. Assumes cipher-text has went through preprocess.
    :param freq: Dict containing the letter frequency distribution.
    :return: TODO!
    """

    # Find the occurrence for each letter
    letter_occurrence = LETTERS
    for letter in cipher_text:
        if letter_occurrence[letter] is None:
            letter_occurrence[letter] = 1
        else:
            letter_occurrence[letter] = letter_occurrence[letter] + 1


    subs = {"e": "9", "a": "1"}
    print("1: " + cipher_text)
    print("2: " + substitute(cipher_text, subs))

    # print freq
    # print letter_occurrence


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
