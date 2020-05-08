import argparse
import random
import utils

from difflib import SequenceMatcher

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class SubstitutionCipher:
    """ Solve substitution cipher using hill climbing approach """
    cipher_text = ""   # Stores the original cipher-text
    key = ""           # Represents the mapping between cipher-text and plain-text letters
    found_the = False  # Did we successfully crack the work 'THE'

    def __init__(self, cipher_text, fitness):
        self.cipher_text = cipher_text  # Prepare input text for decryption

        # Start with a random key
        key = [letter for letter in ALPHABET]
        random.shuffle(key)

        # We can guess 'THE' extremely accurately
        self.found_the = False
        tri = [k for k in utils.get_occurence_dict(utils.get_trigraphs(cipher_text))][0]
        di = [k for k in utils.get_occurence_dict(utils.get_digraphs(cipher_text))][0]
        if di in tri:
            # Successfully found 'THE'
            t_index = key.index(tri[0])  # find the index for letter corresponding to 'T'
            key[t_index], key[19] = key[19], key[t_index]  # T is 19th in alphabet (starting at 0)

            h_index = key.index(tri[1])  # find the index for letter corresponding to 'H'
            key[h_index], key[7] = key[7], key[h_index]  # H is 7th in alphabet (starting at 0)

            e_index = key.index(tri[2])   # find the index for letter corresponding to 'E'
            key[e_index], key[4] = key[4], key[e_index]  # E is 4th in alphabet (starting at 0)
            self.found_the = True

        self.key = "".join(key)  # Convert back to string

        # Calculate log probabilities for mono, di, tri, quadgraphs
        self.mono_prob = utils.get_log_probability(fitness + "monographs.txt")
        self.di_prob = utils.get_log_probability(fitness + "digraphs.txt")
        self.tri_prob = utils.get_log_probability(fitness + "trigraphs.txt")
        self.quad_prob = utils.get_log_probability(fitness + "quadgraphs.txt")

    def solve(self):
        LOOP_LIMIT = 250  # This many failed swaps in a row will stop the algorithm

        iterations = 0
        bad_swaps = 0
        while True:
            iterations += 1
            success = self.key_swap()

            if not success:
                bad_swaps += 1
                if bad_swaps == LOOP_LIMIT:
                    break
            else:
                bad_swaps = 0  # Reset the counter

        print("Iterations: " + str(iterations))
        print("Key:        " + str(self.key))
        print("Ciphertext: " + str(self.cipher_text))
        print("Plaintext:  " + str(self.apply_key()))

        # For testing
        return round(SequenceMatcher(None, self.key, "JDNVPWOZAMXKGIESUTBFQRYHLC").ratio(), 5)

    def apply_key(self):
        """Decrypt the cipher-text using the current key"""
        text = self.cipher_text

        for i in range(len(self.key)):
            text = text.replace(self.key[i], ALPHABET[i].lower())  # We write lowercase so we dont swap characters twice

        return text.upper()  # Return everything to uppercase

    def calculate_fitness(self):
        """
        Calculate the language 'fitness' of the current key(ciphertext)

        Each score is calculated by adding the log probabilities. Ex:
        log(prob(CRYPTO)) = log(prob(CRY)) + log(prob(RYP)) + log(prob(YPT)) + log(prob(PTO))

        Probabilities are negative. Closer to 0 is more likely.
        """
        text = self.apply_key()

        # mono_score = 0
        # monographs = utils.get_monographs(text)
        # for mono in monographs:
        #     # If the substring is not present, the probability is ~0
        #     if mono in self.mono_prob:
        #         mono_score += self.mono_prob[mono]

        di_score = 0
        digraphs = utils.get_digraphs(text)
        for di in digraphs:
            # If the substring is not present, the probability is ~0
            if di in self.di_prob:
                di_score += self.di_prob[di]

        tri_score = 0
        trigraphs = utils.get_trigraphs(text)
        for tri in trigraphs:
            # If the substring is not present, the probability is ~0
            if tri in self.tri_prob:
                tri_score += self.tri_prob[tri]

        quad_score = 0
        quadgraphs = utils.get_quadgraphs(text)
        for quad in quadgraphs:
            # If the substring is not present, the probability is ~0
            if quad in self.quad_prob:
                quad_score += self.quad_prob[quad]

        return di_score + tri_score + (quad_score / 2)
        # return (mono_score / 8) + (di_score / 4) + (tri_score / 2) + quad_score

    def key_swap(self):
        """ Randomly swap key values anc check if that improved the score. """
        old_key = self.key  # In case we need to revert
        old_score = self.calculate_fitness()

        # Do not swap 'THE'
        if not self.found_the:
            options = range(0, 26)
        else:
            options = list(range(0, 4)) + list(range(5, 7)) + list(range(8, 19)) + list(range(20, 26))

        index_1 = random.choice(options)
        index_2 = random.choice(options)
        # Do not allow the same index
        while index_1 == index_2:
            index_2 = random.choice(options)
        list_key = list(self.key)  # Convert to list for swapping
        list_key[index_1], list_key[index_2] = list_key[index_2], list_key[index_1]
        self.key = "".join(list_key)  # Convert back to string

        # Revert if old key had better score (closer to 0, scores are negative)
        if not float(old_score) >= float(self.calculate_fitness()):
            return 1  # Swap was successful

        self.key = old_key
        return 0  # Swap was unsuccessful


if __name__ == "__main__":
    # Parse Args
    parser = argparse.ArgumentParser()
    parser.add_argument('cipher_file', metavar='C', type=str, help="Text file containing the cipher-text.")
    parser.add_argument('--training', dest='training', type=str, default=None,
                        help="Optional: training text to determine language fitness.")
    args = parser.parse_args()

    # Determine what data to calculate language "fitness" with
    fitness_path = "languages/en_us/"  # Use English letter frequencies by default
    # Calculate letter frequencies if they provide training text
    if not args.training is None:
        fitness_path = utils.CUSTOM_FITNESS  # point to custom letter frequencies

        # Read training data
        with open(args.training, 'r') as t_handle:
            training_text = utils.text_preprocessing(t_handle.read())

            # Count frequencies and write to file
            utils.write_custom_fitness_data(training_text)

    # Prepare user inputs for decryption
    with open(args.cipher_file, 'r') as c_handle:
        ct = utils.text_preprocessing(c_handle.read())

    # Solve
    cipher = SubstitutionCipher(cipher_text=ct, fitness=fitness_path)
    cipher.solve()
