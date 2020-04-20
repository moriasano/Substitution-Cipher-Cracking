import argparse
import json

# Used whenever we need to map anything across the entire alphabet
LETTERS = {
    "a": None, "b": None, "c": None, "d": None, "e": None, "f": None, "g": None, "h": None, "i": None,
    "j": None, "k": None, "l": None, "m": None, "n": None, "o": None, "p": None, "q": None, "r": None,
    "s": None, "t": None, "u": None, "v": None, "w": None, "x": None, "y": None, "z": None
}


class Solution:
    """
    Class to represents the in-progress solution as we try to crack the cipher. The solution itself is the list of all
    the substitution (or mappings) for each letter from the cipher-text to the plain-text.
    """
    cipher_text = ""     # Stores the original cipher-text
    substitutions = []   # The list of substitutions, in the order that we add them
    orig_freq = LETTERS  # Contains the occurrence of each letter from the original cipher-text

    def __init__(self, cipher_text):
        self.cipher_text = self.__preprocess(cipher_text)  # Prepare input text for decryption
        self.orig_freq = self.get_occurrences()  # Keep track of the original letter occurrence count

    def push_sub(self, old, new):
        """
        Add a substitution to the in-progress solution.
        :param old: letter from the cipher-text.
        :param new: the letter which the old letter maps to.
        """
        self.substitutions.append((old, new))

    def pop_sub(self):
        """ Remove the newest substitution added. Use this when a mapping we try is wrong. """
        del self.substitutions[-1]

    def substitute(self):
        """
        Perform all of the substitution onto the cipher-text.
        :return: The cipher-text after the substitutions have been performed. With a complete and accurate list of
        substitutions, this should be the complete plain-text.
        """
        pt = [letter for letter in self.cipher_text]

        for orig, sub in self.substitutions:
            i = 0
            for letter in self.cipher_text:
                if letter == orig:
                    pt[i] = sub
                i += 1

        pt = "".join(pt)
        return pt

    def get_occurrences(self):
        """
        Count the occurrence of each letter of the current solution, which it the cipher-text after all substitutions
        have been performed.
        :return: Dict. {Letter: Occurrence}
        """

        # TODO: order this by the occurrence count

        occurrence = LETTERS
        for letter in self.substitute():
            if occurrence[letter] is None:
                occurrence[letter] = 1
            else:
                occurrence[letter] = occurrence[letter] + 1
        return occurrence

    @staticmethod
    def __preprocess(ct):
        """
        Prepare the cipher-text for decryption.
        :param ct: Raw cipher-text
        :return: String ready for decryption.
        """

        # Remove all whitespace
        text = "".join(ct.split())

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
    """
    solution = Solution(cipher_text)
    solution.push_sub(old="i", new="1")
    solution.push_sub(old="e", new="2")
    plain_text = solution.substitute()

    print("orig: " + solution.cipher_text)
    print("new:  " + plain_text)
    print("freq: " + str(solution.orig_freq))


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
            ct = c_handle.read()
            f = json.loads(f_handle.read())

    decrypt(cipher_text=ct, freq=f)
