#!/bin/bash

# Start recording audio using ffmpeg
ffmpeg -f avfoundation -i ":0" -ar 44100 -y output.wav &
echo $! > ffmpeg_pid.txt

echo "Recording started and saving to output.wav"
