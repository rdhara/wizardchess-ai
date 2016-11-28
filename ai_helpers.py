"""
Helper functions for voice recognition and board API calls
"""


import pyaudio
import audioop
import wave
import sys
import math
from collections import deque
"""
Helper functions for voice recognition and board API calls
"""


# intensity threshold to separate silences from voice
THRESHOLD = 1000
SILENCE_LIMIT = 1
PREV_AUDIO = 0.5
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
def get_next_move():
    print "Next move: "
    return str(raw_input())


def get_voice_recording(threshold=THRESHOLD, num_phrases = 2):


    # CHUNK = 1024
    # FORMAT = pyaudio.paInt16
    # CHANNELS = 2
    # RATE = 44100
    # RECORD_SECONDS = 2
    # WAVE_OUTPUT_FILENAME = "output.wav"

    # p = pyaudio.PyAudio()

    # stream = p.open(format=FORMAT,
    #                 channels=CHANNELS,
    #                 rate=RATE,
    #                 input=True,
    #                 frames_per_buffer=CHUNK)

    # print("* recording")

    # frames = []

    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)

    # print("* done recording")

    # stream.stop_stream()
    # stream.close()
    # p.terminate()

    # wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    # wf.setnchannels(CHANNELS)
    # wf.setsampwidth(p.get_sample_size(FORMAT))
    # wf.setframerate(RATE)
    # wf.writeframes(b''.join(frames))
    # wf.close()
    #Open stream
    RECORD_SECONDS = 30
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print "* Listening mic. "
    audio2send = []
    cur_data = ''  # current chunk  of audio data
    rel = RATE/CHUNK
    slid_win = deque(maxlen=SILENCE_LIMIT * rel)
    #Prepend audio from 0.5 seconds before noise was detected
    prev_audio = deque(maxlen=PREV_AUDIO * rel)
    started = False
    n = num_phrases
    response = []

    # while (num_phrases == -1 or n > 0):
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        cur_data = stream.read(CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        #print slid_win[-1]
        if(sum([x > THRESHOLD for x in slid_win]) > 0):
            if(not started):
                print "Starting record of phrase"
                started = True
            audio2send.append(cur_data)
        elif (started is True):
            print "Finished"


            # Reset all
            started = False
            slid_win = deque(maxlen=SILENCE_LIMIT * rel)
            prev_audio = deque(maxlen=0.5 * rel)
            audio2send = []
            n -= 1
        else:
            prev_audio.append(cur_data)

    print "* Done recording"
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
    wf.setframerate(16000)  # TODO make this value a function parameter?
    wf.writeframes(data)
    wf.close()

def interpret_wav():
    pass

get_voice_recording()
"""PyAudio Example: Play a WAVE file."""

CHUNK = 1024

# if len(sys.argv) < 2:
#     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
#     sys.exit(-1)

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
