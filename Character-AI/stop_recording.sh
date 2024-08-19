#!/bin/bash

# Check if ffmpeg is running
if [ -f ffmpeg_pid.txt ]; then
    # Read the PID from the file
    PID=$(cat ffmpeg_pid.txt)
    
    # Send SIGINT to the ffmpeg process to stop recording gracefully
    kill -SIGINT $PID
    
    # Wait for the process to terminate
    wait $PID
    
    # Clean up
    rm ffmpeg_pid.txt
    
    echo "Recording stopped and saved to output.wav"
else
    echo "Recording process not found."
fi
