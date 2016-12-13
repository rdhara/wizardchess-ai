"""
Functions for decoding phonemes using the adapted Sphinx acoustic model
"""

from pocketsphinx import Decoder

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

config = Decoder.default_config()
config.set_string('-hmm', 'en-us-adapt')
config.set_string('-allphone', 'en-us-adapt/chess-phone.lm.bin')
config.set_string('-dict', 'en-us-adapt/chess-project.dic')
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
