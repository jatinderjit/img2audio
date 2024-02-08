import math
import struct

from PIL import Image

img = Image.open("./Computerphile HQ for Dave.png")


values = []
print(img.width, img.height)
for i in range(img.width):
    min_val = math.inf
    max_val = -math.inf
    for j in range(img.height):
        pixel = img.getpixel((i, j))
        green = pixel[1]
        if green > 150:
            min_val = min(min_val, j)
            max_val = max(max_val, j)
    if min_val is not math.inf:
        values.append(min_val)
        values.append(max_val)

FILTER = 4

for i in range(len(values) - FILTER):
    values[i] = sum(values[i : i + FILTER]) // FILTER
# values = values[:-FILTER]

f = open("./output.wav", "wb")

RIFF_HEADER = b"RIFF"
FORMAT_WAVE = b"WAVE"
FORMAT_TAG = b"fmt "
AUDIO_FORMAT = b"\x01\x00"
SUBCHUNK_ID = b"data"
BYTES_PER_SAMPLE = 1
samplerate = 48000
channelcount = 1
lastv2 = 0
stretch = 7
datalength = len(values) * stretch * BYTES_PER_SAMPLE
byteRate = samplerate * channelcount * BYTES_PER_SAMPLE
blockAlign = channelcount * BYTES_PER_SAMPLE

f.write(RIFF_HEADER)
f.write(struct.pack("I", datalength + 40))
f.write(FORMAT_WAVE)
f.write(FORMAT_TAG)
f.write(struct.pack("I", 16))
f.write(AUDIO_FORMAT)
f.write(struct.pack("H", channelcount))
f.write(struct.pack("I", samplerate))
f.write(struct.pack("I", byteRate))
f.write(struct.pack("H", blockAlign))
f.write(struct.pack("H", BYTES_PER_SAMPLE * 8))
f.write(SUBCHUNK_ID)
f.write(struct.pack("I", datalength))

for v in values:
    v2 = (v - min(values)) / (max(values) - min(values)) * 255
    for x in range(stretch):
        v3 = x / stretch * v2 + (1 - x / stretch) * lastv2
        f.write(struct.pack("B", int(v3)))
    lastv2 = int(v2)

f.close()
