import argparse
import random
import utils

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class SubstitutionCipher:
    """
    Class to represents the in-progress solution as we try to crack the cipher. The solution itself is the list of all
    the substitution (or mappings) for each letter from the cipher-text to the plain-text.
    """
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
        plaintext = self.cipher_text

        for i in range(len(self.key)):
            plaintext = plaintext.replace(self.key[i], ALPHABET[i].lower())

        return plaintext.upper()

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

    SubstitutionCipher(cipher_text=ct, fitness=fitness_path)
