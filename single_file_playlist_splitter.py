from pydub import AudioSegment
import re
import os
import argparse
import subprocess

# Function to convert timestamp to milliseconds
def timestamp_to_milliseconds(timestamp):
    parts = list(map(int, timestamp.split(":")))
    if len(parts) == 3:
        hours, minutes, seconds = parts
    else:
        hours = 0
        minutes, seconds = parts
    return ((hours * 60 + minutes) * 60 + seconds) * 1000

# Function to identify audio format
def identify_audio_format(filename):
    return os.path.splitext(filename)[1][1:]

# Define command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("audio_file", help="path to the audio file")
parser.add_argument("txt_file", help='path to the text file with timestamps and song names. each line should be of the format <startMin>:<startSec> "songName" or <startMin>:<startSec> <endMin>:<endSec> "songName" format. In the former case, make sure that songs in sequential lines are sequential in the file too. As in, when one ends, the other starts.')
args = parser.parse_args()

# Load the audio file
audio_format = identify_audio_format(args.audio_file)
#audio = AudioSegment.from_file(args.audio_file, format='opus')
audio = AudioSegment.from_file(args.audio_file, format=audio_format)

# Load timestamps and song names from a text file
with open(args.txt_file, "r") as file:
    lines = file.readlines()

timestamps = []
for i, line in enumerate(lines):
    # Check if the line matches the pattern with an end timestamp
    end_timestamp_match = re.match(r'((?:\d+:)?\d+:\d+) ((?:\d+:)?\d+:\d+) "(.+)"', line.strip())
    
    if end_timestamp_match:
        start_timestamp, end_timestamp, song_name = end_timestamp_match.groups()
        
        # Convert timestamps to milliseconds
        start = timestamp_to_milliseconds(start_timestamp)
        end = timestamp_to_milliseconds(end_timestamp)
    else:
        # Check if the line matches the pattern without an end timestamp
        start_timestamp_match = re.match(r'((?:\d+:)?\d+:\d+) "(.+)"', line.strip())
        
        if start_timestamp_match:
            start_timestamp, song_name = start_timestamp_match.groups()
            
            # Calculate the end timestamp
            if i < len(lines) - 1:  # If not the last song
                next_line_match = re.match(r'((?:\d+:)?\d+:\d+) "(.+)"', lines[i + 1].strip())
                if next_line_match:
                    end_timestamp, _ = next_line_match.groups()
                else:
                    continue  # Invalid next line format, continue to the next song
            else:  # For the last song, use the duration of the audio
                end_timestamp = str(int(audio.duration_seconds // 3600)) + ":" + str(int((audio.duration_seconds % 3600) // 60)) + ":" + str(int(audio.duration_seconds % 60))
            
            # Convert timestamps to milliseconds
            start = timestamp_to_milliseconds(start_timestamp)
            end = timestamp_to_milliseconds(end_timestamp)
        else:
            continue  # Invalid line format, continue to the next song

    # Store in the list
    timestamps.append((start, end, song_name))

def sanitize_filename(filename):
    sanitized_filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    return sanitized_filename

# Split audio file and save the parts
for start, end, song_name in timestamps:
    song_name = sanitize_filename(song_name)
    part = audio[start:end]
    part.export(f"{song_name}.wav", format='wav')
    #part.export(f"{song_name}.{audio_format}", format=audio_format)
    # because for some reason just exporting won't work.
    subprocess.run(["ffmpeg", "-i", f"{song_name}.wav", "-c:a", "aac", f"{song_name}.m4a"])
    # Delete the original WAV file
    os.remove(f"{song_name}.wav")


