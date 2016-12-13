"""
Helper functions to generate input files for CMU Sphinx
"""

# Creating the transcript file for Sphinx

words = ['king', 'queen', 'knight', 'bishop', 'rook', 'pawn',
                 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                 'kingside', 'queenside', 'castle', 'to', 'takes']

file_names = ['king', 'queen', 'knight', 'bishop', 'rook', 'pawn',
                 '1', '2', '3', '4', '5', '6', '7', '8',
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                 'kingside', 'queenside', 'castle', 'to', 'takes']

for word, file_name in zip(words, file_names):
    # construct each line as specified at http://cmusphinx.sourceforge.net/wiki/tutorialam
    line_template = '<s> '
    line_template += word
    line_template += ' </s> ('
    line_template += file_name
    for i in range(1, 51):
        line = line_template + '_' + str(i) + ')'
        print line


# Creating the dictionary file for Sphinx

phoneme_dict = {
    'pawn': ['P', 'AO', 'N'],
    'knight': ['N', 'AY', 'T'],
    'bishop': ['B', 'IH', 'SH', 'AH', 'P'],
    'rook': ['R', 'UH', 'K'],
    'queen': ['K', 'W', 'IY', 'N'],
    'king': ['K', 'IH', 'NG'],
    'takes': ['T', 'EY', 'K', 'S'],
    'side': ['S', 'AY', 'D'],
    'castle': ['K', 'AE', 'S', 'AH', 'L'],
    'one': ['W', 'AH', 'N'],
    'two': ['T', 'UW'],
    'three': ['TH', 'R', 'IY'],
    'four': ['F', 'AO', 'R'],
    'five': ['F', 'AY', 'V'],
    'six': ['S', 'IH', 'K', 'S'],
    'seven': ['S', 'EH', 'V', 'AH', 'N'],
    'eight': ['EY', 'T'],
    'a': ['EY'],
    'b': ['B', 'IY'],
    'c': ['S', 'IY'],
    'd': ['D', 'IY'],
    'e': ['IY'],
    'f': ['EH', 'F'],
    'g': ['JH', 'IY'],
    'h': ['EY', 'CH'],
    'kingside': ['K', 'IH', 'NG', 'S', 'AY', 'D'],
    'queenside': ['K', 'W', 'IY', 'N', 'S', 'AY', 'D'],
    'to': ['T', 'UW']
}

for word in sorted(phoneme_dict):
    print(" ".join([word] + phoneme_dict[word]))

# Creating the configuration file for Sphinx

training_list = ['king', 'queen', 'knight', 'bishop', 'rook', 'pawn',
                 '1', '2', '3', '4', '5', '6', '7', '8',
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                 'kingside', 'queenside', 'castle', 'to', 'takes']
phonemes = {
    'pawn': ['P', 'AO', 'N'],
    'knight': ['N', 'AY', 'T'],
    'bishop': ['B', 'IH', 'SH', 'AH', 'P'],
    'rook': ['R', 'UH', 'K'],
    'queen': ['K', 'W', 'IY', 'N'],
    'king': ['K', 'IH', 'NG'],
    'takes': ['T', 'EY', 'K', 'S'],
    'side': ['S', 'AY', 'D'],
    'castle': ['K', 'AE', 'S', 'AH', 'L'],
    '1': ['W', 'AH', 'N'],
    '2': ['T', 'UW'],
    '3': ['TH', 'R', 'IY'],
    '4': ['F', 'AO', 'R'],
    '5': ['F', 'AY', 'V'],
    '6': ['S', 'IH', 'K', 'S'],
    '7': ['S', 'EH', 'V', 'AH', 'N'],
    '8': ['EY', 'T'],
    '9': ['N', 'AY', 'N'],
    'a': ['EY'],
    'b': ['B', 'IY'],
    'c': ['S', 'IY'],
    'd': ['D', 'IY'],
    'e': ['IY'],
    'f': ['EH', 'F'],
    'g': ['JH', 'IY'],
    'h': ['EY', 'CH'],
    'kingside': ['K', 'IH', 'NG', 'S', 'AY', 'D'],
    'queenside': ['K', 'W', 'IY', 'N', 'S', 'AY', 'D'],
    'to': ['T', 'UW']
}

for word in training_list:
    for _ in range(50):
        print(" ".join(phonemes[word]))
