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
    orig_mono_freq = []  # Contains the occurrence of each letter from the original cipher-text
    orig_di_freq = []    # Contains the occurrence of each digraph from the original cipher-text
    orig_tri_freq = []   # Contains the occurrence of each trigraph from the original cipher-text

    def __init__(self, cipher_text):
        self.cipher_text = self.__preprocess(cipher_text)  # Prepare input text for decryption
        self.orig_mono_freq = self.get_mono_freq()  # Keep track of the original letter count
        self.orig_di_freq = self.get_di_freq()      # Keep track of the original digraph count
        self.orig_tri_freq = self.get_tri_freq()    # Keep track of the original digraph count

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

    def get_mono_freq(self):
        """
        Count the occurrence of each letter of the current solution, which it the cipher-text after all substitutions
        have been performed.
        :return: List of (Letter:, Occurrence)
        """
        occurrences = LETTERS
        for letter in self.substitute():
            if occurrences[letter] is None:
                occurrences[letter] = 1
            else:
                occurrences[letter] = occurrences[letter] + 1

        # Put in descending order
        occurrences = sorted(occurrences.iteritems(), key=lambda x: x[1], reverse=True)

        return occurrences

    def get_di_freq(self):
        """
        Count the occurrence of each digraph of the current solution, which it the cipher-text after all substitutions
        have been performed.
        :return: List of (Digraph:, Occurrence)
        """
        occurrences = {}
        text = self.substitute()
        for i in range(len(text) - 1):
            di = text[i] + text[i + 1]

            if di in occurrences:
                occurrences[di] = occurrences[di] + 1
            else:
                occurrences[di] = 1

        # Put in descending order
        occurrences = sorted(occurrences.iteritems(), key=lambda x: x[1], reverse=True)

        return occurrences

    def get_tri_freq(self):
        """
        Count the occurrence of each trigraph of the current solution, which it the cipher-text after all substitutions
        have been performed.
        :return: List of (Trigraph:, Occurrence)
        """
        occurrences = {}
        text = self.substitute()
        for i in range(len(text) - 2):
            tri = text[i] + text[i + 1] + text[i + 2]

            if tri in occurrences:
                occurrences[tri] = occurrences[tri] + 1
            else:
                occurrences[tri] = 1

        # Put in descending order
        occurrences = sorted(occurrences.iteritems(), key=lambda x: x[1], reverse=True)

        return occurrences

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


def crack(cipher_text, mono, di, tri):
    """
    Main algorithm flow for cracking.
    :param cipher_text: The cipher-text as a string. Assumes cipher-text has went through preprocess.
    :param mono: list of sorted monograms.
    :param di: list of sorted digraphs.
    :param tri: list of sorted trigraphs.
    """
    solution = Solution(cipher_text)

    print("mono: " + str(solution.orig_mono_freq))
    print("di:   " + str(solution.orig_di_freq))
    print("tri:  " + str(solution.orig_tri_freq))

    # Start with the word "THE"
    

    # # Just try substituting in order of frequency json
    # for i in range(len(mono)):
    #     old = solution.orig_mono_freq[i][0]
    #     new = str(mono[i][0])
    #     print(old + " is probably '" + new + "'.")
    #     solution.push_sub(old=old, new=new)

    # plain_text = solution.substitute()
    # print("orig: " + solution.cipher_text)
    # print("new:  " + plain_text)



if __name__ == "__main__":
    # Parse Args
    parser = argparse.ArgumentParser()
    parser.add_argument('cipher_file', metavar='C', type=str, help="Text file containing the cipher-text.")
    parser.add_argument('--lang', dest='lang', type=str, default="frequencies/us_english.json",
                        help="Optional: possible support for other languages in the future.")
    args = parser.parse_args()

    # Prepare user inputs for decryption
    with open(args.cipher_file, 'r') as c_handle:
        ct = c_handle.read()
    with open(args.lang, 'r') as f_handle:
        f = json.loads(f_handle.read())

        # Read in frequencies from file
        m = sorted(f["monograms"].iteritems(), key=lambda x: x[1], reverse=True)
        d = sorted(f["digraphs"].iteritems(), key=lambda x: x[1], reverse=True)
        t = sorted(f["trigraph"].iteritems(), key=lambda x: x[1], reverse=True)

    crack(cipher_text=ct, mono=m, di=d, tri=t)
