import argparse
import itertools
import json


class Solution:
    """
    Class to represents the in-progress solution as we try to crack the cipher. The solution itself is the list of all
    the substitution (or mappings) for each letter from the cipher-text to the plain-text.
    """
    cipher_text = ""        # Stores the original cipher-text
    substitutions = {}      # The list of substitutions, in the order that we add them

    def __init__(self, cipher_text):
        self.cipher_text = self.__preprocess(cipher_text)  # Prepare input text for decryption
        self.substitutions = {letter: [] for letter in alphabet}

    def add_sub(self, c_letter, p_letter):
        """
        Add a substitution to the in-progress solution.
        :param c_letter: letter from the cipher-text.
        :param p_letter: the letter which the old letter maps to.
        """
        self.substitutions[c_letter].append(p_letter)

    def del_sub(self, c_letter, p_letter):
        """
        Remove a possible substitution from the in-progress solution.
        :param c_letter: letter from the cipher-text.
        :param p_letter: the letter which the old letter maps to.
        """
        try:
            self.substitutions[c_letter].remove(p_letter)
        except ValueError:
            print("{} is not in the substitution list for {}".format(p_letter, c_letter))

    def substitute(self):
        """ Get all possible plain-texts, given the substitutions added to the solution so far """
        possible_plaintexts = []

        # TODO: remove permutations with repeated letters

        # Get list of all possible permutations of substitutions
        letters_with_subs = [letter for letter in self.substitutions if len(self.substitutions[letter]) > 0]
        list_of_subs = [self.substitutions[letter] for letter in letters_with_subs]
        for l in list(itertools.product(*list_of_subs)):
            substitutions = {letters_with_subs[i]: l[i] for i in range(len(letters_with_subs))}

            # Perform the substitutions
            plaintext = list(self.cipher_text)
            for key in substitutions:
                i = 0
                for letter in self.cipher_text:
                    if letter == key:
                        plaintext[i] = substitutions[key]
                    i += 1
            plaintext = "".join(plaintext)

            possible_plaintexts.append(plaintext)

        return possible_plaintexts

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


def get_mono_freq(string):
    """
    Count the occurrence of each letter of the current solution, which it the cipher-text after all substitutions
    have been performed.
    :return: List of (Letter:, Occurrence)
    """
    occurrences = {letter: 0 for letter in alphabet}

    for letter in string:
        occurrences[letter] = occurrences[letter] + 1

    # Put in descending order
    occurrences = sorted(occurrences.iteritems(), key=lambda x: x[1], reverse=True)

    return occurrences


def get_di_freq(string):
    """
    Count the occurrence of each digraph of the current solution, which it the cipher-text after all substitutions
    have been performed.
    :return: List of (Digraph:, Occurrence)
    """
    occurrences = {}

    for i in range(len(string) - 1):
        di = string[i] + string[i + 1]

        if di in occurrences:
            occurrences[di] = occurrences[di] + 1
        else:
            occurrences[di] = 1

    # Put in descending order
    occurrences = sorted(occurrences.iteritems(), key=lambda x: x[1], reverse=True)

    return occurrences


def get_tri_freq(string):
    """
    Count the occurrence of each trigraph of the current solution, which it the cipher-text after all substitutions
    have been performed.
    :return: List of (Trigraph:, Occurrence)
    """
    occurrences = {}

    for i in range(len(string) - 2):
        tri = string[i] + string[i + 1] + string[i + 2]

        if tri in occurrences:
            occurrences[tri] = occurrences[tri] + 1
        else:
            occurrences[tri] = 1

    # Put in descending order
    occurrences = sorted(occurrences.iteritems(), key=lambda x: x[1], reverse=True)

    return occurrences


def crack(cipher_text, mono, di, tri):
    """
    Main algorithm flow for cracking.
    :param cipher_text: The cipher-text as a string. Assumes cipher-text has went through preprocess.
    :param mono: list of sorted monograms.
    :param di: list of sorted digraphs.
    :param tri: list of sorted trigraphs.
    """

    # This is where we will store the solution
    solution = Solution(cipher_text)

    # Count the mono, di, and trigraphs
    mono = get_mono_freq(solution.cipher_text)
    di = get_di_freq(solution.cipher_text)
    tri = get_tri_freq(solution.cipher_text)

    print("mono: " + str(mono))
    print("di:   " + str(di))
    print("tri:  " + str(tri))

    # Start with the word "THE"
    mono_1 = mono[0][0]  # This should be 'e'
    di_1 = di[0][0]      # This should be 'th'
    tri_1 = tri[0][0]    # This should be 'the'
    top_5 = [letter for letter, freq in mono][0:5]  # Top 5 most frequent cipher-text letters
    if mono_1 in tri_1 and di_1 in tri_1:
        if di_1 + mono_1 == tri_1:
            # Best case scenario which matches frequencies perfectly; di = th, mono = e
            print("Found 'THE' - Best Case")
        elif di_1 in tri_1 and tri_1[0] in top_5:
            # Okay scenario which matches frequencies closely; di = he, mono = e
            print("Fount 'THE' - Good Case")

        solution.add_sub(tri_1[0], "T")
        solution.add_sub(tri_1[1], "H")
        solution.add_sub(tri_1[2], "E")
    else:
        print("Did not find 'THE'")

    for sol in solution.substitute():
        print(sol)


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

    # Define the alphabet from the list of monograms
    global alphabet
    alphabet = [letter for letter, _ in m]
    alphabet.sort()

    crack(cipher_text=ct, mono=m, di=d, tri=t)
