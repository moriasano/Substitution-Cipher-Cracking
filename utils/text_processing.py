
def text_preprocessing(text):
    """ Prepare text for processing. """
    text = ''.join([i for i in text if i.isalpha()])  # Remove all non-alphabet characters
    text = text.upper()  # Uppercase

    return text


def count_custom_fitness_data(training_text):
    # TODO: you are here!!!! Count all the mono, di, tri, quadgraphes and write to file