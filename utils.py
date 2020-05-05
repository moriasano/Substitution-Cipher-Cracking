import math

CUSTOM_FITNESS = "languages/custom/"  # Custom letter training is written here

def text_preprocessing(text):
    """ Prepare text for processing. """
    text = ''.join([i for i in text if i.isalpha()])  # Remove all non-alphabet characters
    text = text.upper()  # Uppercase

    return text

def get_monographs(text):
    monographs = []

    for letter in text:
        monographs.append(letter)

    return monographs

def get_digraphs(text):
    digraphs = []

    for i in range(len(text) - 1):
        digraphs.append(text[i:i + 2])

    return digraphs

def get_trigraphs(text):
    trigraphs = []

    for i in range(len(text) - 2):
        trigraphs.append(text[i:i + 3])

    return trigraphs

def get_quadgraphs(text):
    quadgraphs = []

    for i in range(len(text) - 3):
        quadgraphs.append(text[i:i + 4])

    return quadgraphs

def write_custom_fitness_data(training_text):

    # Monographs
    mono_count = {}
    monographs = get_monographs(training_text)
    for mono in monographs:
        if mono in mono_count:
            mono_count[mono] += 1
        else:
            mono_count[mono] = 1
    with open(CUSTOM_FITNESS + "monographs.txt", 'w') as fh:
        sorted_count = {k: v for k, v in sorted(mono_count.items(), key=lambda item: item[1], reverse=True)}
        for key in sorted_count:
            fh.write("{} {}\n".format(str(key), str(sorted_count[key])))

    # Digraphs
    di_count = {}
    digraphs = get_digraphs(training_text)
    for di in digraphs:
        if di in di_count:
            di_count[di] += 1
        else:
            di_count[di] = 1
    with open(CUSTOM_FITNESS + "digraphs.txt", 'w') as fh:
        sorted_count = {k: v for k, v in sorted(di_count.items(), key=lambda item: item[1], reverse=True)}
        for key in sorted_count:
            fh.write("{} {}\n".format(str(key), str(sorted_count[key])))

    # Trigraphs
    tri_count = {}
    trigraphs = get_trigraphs(training_text)
    for tri in trigraphs:
        if tri in tri_count:
            tri_count[tri] += 1
        else:
            tri_count[tri] = 1
    with open(CUSTOM_FITNESS + "trigraphs.txt", 'w') as fh:
        sorted_count = {k: v for k, v in sorted(tri_count.items(), key=lambda item: item[1], reverse=True)}
        for key in sorted_count:
            fh.write("{} {}\n".format(str(key), str(sorted_count[key])))

    quad_count = {}
    quadgraphs = get_quadgraphs(training_text)
    for quad in quadgraphs:
        if quad in quad_count:
            quad_count[quad] += 1
        else:
            quad_count[quad] = 1
    with open(CUSTOM_FITNESS + "quadgraphs.txt", 'w') as fh:
        sorted_count = {k: v for k, v in sorted(quad_count.items(), key=lambda item: item[1], reverse=True)}
        for key in sorted_count:
            fh.write("{} {}\n".format(str(key), str(sorted_count[key])))

def get_log_probability(file):
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
