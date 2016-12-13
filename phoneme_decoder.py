"""
Functions for decoding phonemes using the adapted Sphinx acoustic model
"""

import glob
import os
from multiprocessing import Pool
from pocketsphinx import DefaultConfig, Decoder, get_model_path, get_data_path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
from tqdm import *



MODELDIR = get_model_path()
DATADIR = get_data_path()


config = Decoder.default_config()
config.set_string('-hmm', os.path.join(MODELDIR, 'en-us-adapt'))
config.set_string('-allphone', os.path.join(MODELDIR, 'chess-phone.lm.bin'))
config.set_string('-dict', '/Users/chrischen/CS182/wechess-ai/chess-project.dic')
config.set_float('-lw', 2.0)
config.set_float('-beam', 1e-10)
config.set_float('-pbeam', 1e-10)

# Decode streaming data.
decoder = Decoder(config)


def get_phonemes(file):
    # Decode streaming data
    decoder = Decoder(config)
    decoder.start_utt()
    stream = open(file, 'rb')
    i=0
    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
    decoder.end_utt()

    Hypothesis = decoder.hyp()
    return [seg.word for seg in decoder.seg()]

file_list = [i for i in glob.glob('wav/*') if '.wav' in i]

# Import phonemes of training sets
training_set = {}
for w in words:
    training_set[w] = []


# For each file name
def get_phoneme_pool(filepath):
    return (filepath.split('/wav/')[1].split('_')[0], get_phonemes(filepath))


def run_pool():
    pool_party = Pool(processes=2)

    for res in tqdm(pool_party.imap_unordered(get_phoneme_pool, file_list)):
        training_set[res[0]].append(res[1])
