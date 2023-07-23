import os
import re
import argparse
from mutagen.id3 import ID3, TIT2, TPE1
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggopus import OggOpus, OggOpusVComment

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--approve", help="approve each metadata change. typing $f instead of the new title, if you are asked, is a shorthand for making the title the filename.", action="store_true")
parser.add_argument("-f", "--folder", help="use the last folder's name as the artist name", action="store_true")
parser.add_argument("-d", "--directory", help="specify the directory containing the files. DEFAULT is this file's directory", type=str, default=os.getcwd())
args = parser.parse_args()

# Regular expression for "<ARTIST> ...some spaces... - ...spaces... <SONG>" or "<ARTIST> _ <SONG>"
pattern = re.compile(r'^(.+?)\s+[-_]?\s+(.+)(\..*)$')

# Directory with your files
#directory = r'C:\Users\Halil\Music\ydl-downloads\Mazhar Fuat Ozkan (MFO)'
directory = args.directory

# Get the last folder's name if the folder flag is set
if args.folder:
    artist = os.path.basename(directory)
else:
    artist = "Default Artist"

# Loop through all files in the directory
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    
    # Extract the artist and title from the filename
    match = pattern.match(filename)
    if match:
        title = match.group(2)
        if not args.folder:
            artist = match.group(1)
    else:
        title = os.path.splitext(filename)[0]

    if filename.endswith(".mp3"):  # Check if it's an mp3
        audio = MP3(file_path, ID3=ID3)
        tag_title = TIT2(encoding=3, text=title)
        tag_artist = TPE1(encoding=3, text=artist)

    elif filename.endswith(".m4a"):  # Check if it's an m4a
        audio = MP4(file_path)
        tag_title = "\xa9nam"
        tag_artist = "\xa9ART"

    elif filename.endswith(".opus"):  # Check if it's an opus
        audio = OggOpus(file_path)

        # Make sure the tags object exists
        if audio.tags is None:
            audio.tags = audio.add_tags()        
        # Assign tag title and artist for opus files
        tag_title = "TITLE"
        tag_artist = "ARTIST"
    
    else:
        continue

    if args.approve:
        print(f"File: {filename}")
        print(f"Proposed Title: {title}")
        print(f"Proposed Artist: {artist}")
        confirm = input("Approve? (Y/N) ")
        if confirm.lower() == "n":
            if args.folder:
                title = input("Enter new title (keep empty or enter $f to use filename): ")
            else:
                title = input("Enter new title (keep empty or enter $f to use filename): ")
                artist = input("Enter new artist: ")
            if title == r'$f' or title == '':
                try:
                    title = match.group(1) + " - " + match.group(2)
                except:
                    # get the full filename, then.
                    pattern = re.compile(r'^(.+?)(\..*)$')
                    match = pattern.match(filename)
                    title = match.group(1)
        elif confirm.lower() != "y":
            continue
    
    # Add the title and artist tags
    audio[tag_title] = title
    audio[tag_artist] = artist

    # Save the changes
    audio.save()

print("Metadata updated for all files.")
