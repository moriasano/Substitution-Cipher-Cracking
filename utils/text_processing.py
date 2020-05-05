CUSTOM_FITNESS = "languages/custom/"  # Custom letter training is written here

def text_preprocessing(text):
    """ Prepare text for processing. """
    text = ''.join([i for i in text if i.isalpha()])  # Remove all non-alphabet characters
    text = text.upper()  # Uppercase

    return text


def count_custom_fitness_data(training_text):
    # TODO: you are here!!!! Count all the mono, di, tri, quadgraphes and write to file

    mono_count = {}
    di_count = {}
    tri_count = {}
    quad_count = {}

    for i in range(len(training_text) - 3):
        mono = training_text[i]
        di = training_text[i:i + 2]
        tri = training_text[i:i + 3]
        quad = training_text[i:i + 4]

        # Increment Mono, Di, Tri, Quadgraphs
        if mono in mono_count:
            mono_count[mono] += 1
        else:
            mono_count[mono] = 1

        if di in di_count:
            di_count[di] += 1
        else:
            di_count[di] = 1

        if tri in tri_count:
            tri_count[tri] += 1
        else:
            tri_count[tri] = 1

        if quad in quad_count:
            quad_count[quad] += 1
        else:
            quad_count[quad] = 1

        # TODO: The above does not count the last 3 characters, add this later if time permits

    # Write counts to file
    with open(CUSTOM_FITNESS + "monographs.txt", 'w') as fh:
        sorted_count = {k: v for k, v in sorted(mono_count.items(), key=lambda item: item[1], reverse=True)}
        for key in sorted_count:
            fh.write("{} {}\n".format(str(key), str(sorted_count[key])))
    with open(CUSTOM_FITNESS + "digraphs.txt", 'w') as fh:
        sorted_count = {k: v for k, v in sorted(di_count.items(), key=lambda item: item[1], reverse=True)}
        for key in sorted_count:
            fh.write("{} {}\n".format(str(key), str(sorted_count[key])))
    with open(CUSTOM_FITNESS + "trigraphs.txt", 'w') as fh:
        sorted_count = {k: v for k, v in sorted(tri_count.items(), key=lambda item: item[1], reverse=True)}
        for key in sorted_count:
            fh.write("{} {}\n".format(str(key), str(sorted_count[key])))
    with open(CUSTOM_FITNESS + "quadgraphs.txt", 'w') as fh:
        sorted_count = {k: v for k, v in sorted(quad_count.items(), key=lambda item: item[1], reverse=True)}
        for key in sorted_count:
            fh.write("{} {}\n".format(str(key), str(sorted_count[key])))