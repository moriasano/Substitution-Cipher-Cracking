import argparse
import random
import utils

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class SubstitutionCipher:
    """ Solve substitution cipher using hill climbing approach """
    cipher_text = ""  # Stores the original cipher-text
    key = ""          # Represents the mapping between cipher-text and plain-text letters

    def __init__(self, cipher_text, fitness):
        self.cipher_text = cipher_text  # Prepare input text for decryption

        # Start with a random key
        key = [letter for letter in ALPHABET]
        random.shuffle(key)
        self.key = "".join(key)

        # Calculate log probabilities for mono, di, tri, quadgraphs
        self.mono_prob = utils.get_log_probability(fitness + "monographs.txt")
        self.di_prob = utils.get_log_probability(fitness + "digraphs.txt")
        self.tri_prob = utils.get_log_probability(fitness + "trigraphs.txt")
        self.quad_prob = utils.get_log_probability(fitness + "quadgraphs.txt")

    def solve(self):
        ROUNDS = 5000

        for _ in range(ROUNDS):
            self.key_swap()

        return self.apply_key()

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

        mono_score = 0
        monographs = utils.get_monographs(text)
        for mono in monographs:
            # If the substring is not present, the probability is ~0
            if mono in self.mono_prob:
                mono_score += self.mono_prob[mono]

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

        # TODO: What is the best way to calculate a total score

        return mono_score + di_score + tri_score + quad_score

    def key_swap(self):
        """ Randomly swap key values anc check if that improved the score. """
        old_key = self.key  # In case we need to revert
        old_score = self.calculate_fitness()

        index_1 = random.randint(0, 25)
        index_2 = random.randint(0, 25)
        # Do not allow the same index
        while index_1 == index_2:
            index_2 = random.randint(0, 25)
        list_key = list(self.key)  # Convert to list for swapping
        list_key[index_1], list_key[index_2] = list_key[index_2], list_key[index_1]
        self.key = "".join(list_key)  # Convert back to string

        # Revert if old key had better score (closer to 0, scores are negative)
        if old_score > self.calculate_fitness():
            self.key = old_key


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

    cipher = SubstitutionCipher(cipher_text=ct, fitness=fitness_path)
    print(cipher.solve())