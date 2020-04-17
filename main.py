import sys


def preprocess(text):
    """
    Check that format and character set are valid before cracking
    :param text: cipher-text as a string
    :return: the properly formatted cipher-text
    """
    # Remove all whitespace
    text = text.replace(" ", "").replace("\n", "").replace("\t", "")

    # Check that text is only alphabet characters
    if not text.isalpha():
        raise ValueError("Cipher-text must only contain English alphabet characters.")

    # Make everything upper-case for consistency
    text = text.upper()

    return text


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as fh:
        cipher_text = fh.read()

    print(preprocess(cipher_text))
