import numpy as np
import sounddevice as sd
import os
import shutil
import time

# basic settings
# You will need to edit the SAMPLE_RATE and another value in line 34
SAMPLE_RATE = 48000 # Run temp.py script to check all your available devices, then copy the sample rate of your output device and paste here
BLOCK_SIZE = 1024
REFRESH_RATE = 1 / 30 
NUM_BARS = 80
CHAR_HEIGHT = 20
BAR_CHAR = "█"

def get_terminal_size():
    size = shutil.get_terminal_size((80, 24))
    return size.columns, size.lines

buffer = np.zeros(BLOCK_SIZE)

def audio_callback(indata, frames, time_info, status):
    global buffer
    buffer = indata[:, 0]

def render_bars(data, width, height):
    spectrum = np.abs(np.fft.rfft(data * np.hanning(len(data))))
    spectrum = spectrum[:NUM_BARS]
    spectrum = spectrum / (np.max(spectrum) + 1e-6)
    spectrum = spectrum ** 2.2
    bars = (spectrum * height).astype(int)
    return bars

stream = sd.InputStream(callback=audio_callback, device=15, channels=2, samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE)
stream.start()

try:
    while True:
        width, term_height = get_terminal_size()
        bar_height = min(CHAR_HEIGHT, term_height - 2)
        bars = render_bars(buffer, width, bar_height)

        os.system("cls" if os.name == "nt" else "clear")

        for row in range(bar_height, 0, -1):
            line = ""
            for val in bars:
                line += BAR_CHAR if val >= row else " "
            print(line)

        time.sleep(REFRESH_RATE)
except KeyboardInterrupt:
    pass
finally:
    stream.stop()
