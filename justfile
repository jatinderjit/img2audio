run:
    # mv ~/Pictures/Screenshots/shottr/sample-audio-wave.png /tmp/sample-audio-wave.png
    python ./img2audio.py
    ffmpeg -y -i output.wav output.mp3
