"""
Helper functions for voice recognition and board API calls
"""


import pyaudio
import audioop
import wave
import math
from collections import deque


# intensity threshold to separate silences from voice
THRESHOLD = 2000
SILENCE_LIMIT = 1
PREV_AUDIO = 0.5
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024


def get_voice_recording(threshold=THRESHOLD):

    RECORD_SECONDS = 5
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
    slid_win = deque()
    prev_audio = deque()
    started = False

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        cur_data = stream.read(CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        if sum([x > THRESHOLD for x in slid_win]) > 0:
            if not started:
                print("Starting record of phrase")
                started = True
            audio2send.append(cur_data)
        elif started:
            print("Finished")
            started = False
            slid_win = deque()
            prev_audio = deque()
            audio2send = []
        else:
            prev_audio.append(cur_data)

    print("* Done recording")
    save_speech(list(prev_audio) + audio2send, p)


def save_speech(data, p):
    """ Saves mic data to temporary WAV file. Returns filename of saved
        file """

    filename = 'output'
    # writes data to WAV file
    data = ''.join(data)
    wf = wave.open(filename + '.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
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
