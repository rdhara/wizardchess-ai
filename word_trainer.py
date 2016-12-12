"""
Find transition probabilities from audio input
"""

import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000


def record_audio(n_sec=5, output=None):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * n_sec)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    if output:
        wf = wave.open(output, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    return frames

training_list = ['king', 'queen', 'knight', 'bishop', 'rook', 'pawn',
                 '1', '2', '3', '4', '5', '6', '7', '8',
                 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                 'kingside', 'queenside', 'castle', 'to', 'takes']

for i in range(23, 25):
    for item in training_list:
        if len(item) > 2:
            rec_time = 2
        else:
            rec_time = 1.5
        print('SAY: ' + item)
        record_audio(n_sec=rec_time, output='training/{}_{}.wav'.format(item, i+1))
