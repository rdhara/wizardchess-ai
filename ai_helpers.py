"""
Helper functions and definitions for voice recognition and board API calls
"""

from collections import Counter

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
    'queenside': ['K', 'W', 'IY', 'N', 'S', 'AY', 'D']
}


# return a dictionary mapping phonemes to their frequencies
def get_phoneme_frequencies(phonemes):
    # Counter to store phoneme frequencies
    freqs = Counter()
    # increment the counter for each phoneme
    for list in phonemes.values():
        for phoneme in list:
            freqs[phoneme] += 1
    return dict(freqs)


# return a dictionary mapping word to P(word|phoneme) for all words
def get_conditional_probabilities(phonemes):
    freqs = get_phoneme_frequencies(phonemes)
    p_words_given_phonemes = {}
    # for each phoneme
    for phoneme in freqs:
        # count how many time each phoneme appears across all words
        p_word_given_phoneme = Counter()
        for word in phonemes:
            for word_phoneme in phonemes[word]:
                if word_phoneme == phoneme:
                    p_word_given_phoneme[word] += 1
        # divide by the total number of occurrences for each phoneme
        for word in p_word_given_phoneme.keys():
            p_word_given_phoneme[word] /= 1.0 * freqs[phoneme]
        p_words_given_phonemes[phoneme] = dict(p_word_given_phoneme)
    return p_words_given_phonemes
