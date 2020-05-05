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
        """
        text = self.apply_key()

        mono_score = 0
        monographs = utils.get_monographs(text)
        for mono in monographs:
            mono_score += self.mono_prob[mono]

        di_score = 0
        digraphs = utils.get_digraphs(text)
        for di in digraphs:
            di_score += self.di_prob[di]

        tri_score = 0
        trigraphs = utils.get_trigraphs(text)
        for tri in trigraphs:
            tri_score += self.tri_prob[tri]

        quad_score = 0
        quadgraphs = utils.get_quadgraphs(text)
        for quad in quadgraphs:
            quad_score += self.quad_prob[quad]


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
    cipher.calculate_fitness()