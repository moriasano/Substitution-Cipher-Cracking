import math

CUSTOM_FITNESS = "languages/custom/"  # Custom letter training is written here

def text_preprocessing(text):
    """ Prepare text for processing. """
    text = ''.join([i for i in text if i.isalpha()])  # Remove all non-alphabet characters
    text = text.upper()  # Uppercase

    return text

def get_monographs(text):
    """ Get list of monographs """
    monographs = []

    for letter in text:
        monographs.append(letter)

    return monographs

def get_digraphs(text):
    """ Get list of digraphs """
    digraphs = []

    for i in range(len(text) - 1):
        digraphs.append(text[i:i + 2])

    return digraphs

def get_trigraphs(text):
    """ Get list of trigraphs """
    trigraphs = []

    for i in range(len(text) - 2):
        trigraphs.append(text[i:i + 3])

    return trigraphs

def get_quadgraphs(text):
    """ Get list of quadgraphs """
    quadgraphs = []

    for i in range(len(text) - 3):
        quadgraphs.append(text[i:i + 4])

    return quadgraphs

def get_occurence_dict(list):
    """ Convert a list of substring into a dictionary of substring and there counts"""
    count = {}

    for substring in list:
        if substring in count:
            count[substring] += 1
        else:
            count[substring] = 1

    # Return the dictionary in descending order
    return {k: v for k, v in sorted(count.items(), key=lambda item: item[1], reverse=True)}

def write_custom_fitness_data(training_text):
    """ Allow for custom probabilities by counting occurrences in user provided text. """

    # Monographs
    monograph_dict = get_occurence_dict(get_monographs(training_text))
    with open(CUSTOM_FITNESS + "monographs.txt", 'w') as fh:
        for key in monograph_dict:
            fh.write("{} {}\n".format(str(key), str(monograph_dict[key])))

    # Digraphs
    digraph_dict = get_occurence_dict(get_digraphs(training_text))
    with open(CUSTOM_FITNESS + "digraphs.txt", 'w') as fh:
        for key in digraph_dict:
            fh.write("{} {}\n".format(str(key), str(digraph_dict[key])))

    # Trigraphs
    trigraph_dict = get_occurence_dict(get_trigraphs(training_text))
    with open(CUSTOM_FITNESS + "trigraphs.txt", 'w') as fh:
        for key in trigraph_dict:
            fh.write("{} {}\n".format(str(key), str(trigraph_dict[key])))

    # Quadgraph
    quadgraph_dict = get_occurence_dict(get_quadgraphs(training_text))
    with open(CUSTOM_FITNESS + "quadgraphs.txt", 'w') as fh:
        for key in quadgraph_dict:
            fh.write("{} {}\n".format(str(key), str(quadgraph_dict[key])))

def get_log_probability(file):
    """ File contains substring and counts. Convert that into log probabilities. """
    total_count = 0
    log_probability = {}

    # Read statistics
    with open(file, 'r') as fh:
        line = fh.readline()
        while line:
            key, count = line.split(" ")
            log_probability[key] = count
            total_count += int(count)

            # Next line of file
            line = fh.readline()

    for key in log_probability:
        log_probability[key] = math.log(int(log_probability[key]) / int(total_count))

    return log_probability
