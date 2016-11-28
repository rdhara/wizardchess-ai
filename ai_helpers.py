"""
Helper functions for voice recognition and board API calls
"""


import pyaudio
import audioop
import wave
import math
from collections import deque


# intensity threshold to separate silences from voice
THRESHOLD = 500
SILENCE_LIMIT = 1
PREV_AUDIO = 0.5
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024


def get_voice_recording(threshold=THRESHOLD):

    RECORD_SECONDS = 7
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* Listening mic. ")
    audio2send = []
    cur_data = ''
    rel = RATE/CHUNK
    slid_win = deque(maxlen=SILENCE_LIMIT * rel)
    prev_audio = deque()
    started = False
    phrase = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        cur_data = stream.read(CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        if sum([x > THRESHOLD for x in slid_win]) > 0:
            if not started:
                print("Starting record of phrase")
                phrase = []
                started = True
            phrase.append(cur_data)
        elif started:
            print("Finished")
            started = False
            slid_win = deque(maxlen=SILENCE_LIMIT * rel)
            audio2send.append(phrase)
            prev_audio = deque()
        else:
            prev_audio.append(cur_data)

    print("Finished")
    audio2send.append(phrase)

    print("* Done recording")
    print len(audio2send)
    save_speech(audio2send + [list(prev_audio)], p)


def save_speech(data, p):
    """ Saves mic data to temporary WAV file. Returns filename of saved
        file """

    filename = 'output'
    # writes data to WAV file
    data = ''.join([item for sublist in data for item in sublist])
    wf = wave.open(filename + '.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(data)
    wf.close()


def interpret_wav():
    pass

get_voice_recording()
"""PyAudio Example: Play a WAVE file."""

CHUNK = 1024

wf = wave.open("output.wav", 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()
