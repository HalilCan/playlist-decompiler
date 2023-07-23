import subprocess
import argparse
import os
import yt_dlp

# Create the argument parser for this script
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--approve", help="approve each metadata change. typing $f instead of the new title, if you are asked, is a shorthand for making the title the filename.", action="store_true")
parser.add_argument("-f", "--folder", help="use the last folder's name as the artist name", action="store_true")
parser.add_argument("-d", "--directory", help="specify the directory containing the files. DEFAULT is this file's directory", type=str, default=os.getcwd())
parser.add_argument("txt_file", help='path to the text file with timestamps and song names.')
parser.add_argument("video_url", help="URL of the video to download.")
args = parser.parse_args()

# Get the video title
ydl_opts = {}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(args.video_url, download=False)
    video_title = info_dict.get('title', None)

# Format the title to create filename (replace unallowed characters)
video_title = "downloaded_playlist"
audio_file = f"{video_title}.m4a"

# Download video
subprocess.run(['youtube-dl-nightly', '-o', f"{video_title}.%(ext)s", 'bestaudio[ext=m4a]/bestaudio/best', '--extract-audio', '--audio-quality', '0', '--xattrs', '--ignore-errors', args.video_url], check=True)

# Run the name_tilde_destroyer.sh to clean up the file name.
subprocess.run(['sh', 'name_tilde_destroyer.sh'], check=True)

# Run the opus_to_m4a_converter.sh to convert for ffmpeg manipulations.
subprocess.run(['sh', 'opus_to_m4a_converter.sh'], check=True)

# Run single_file_playlist_splitter.py
subprocess.run(['python3', 'single_file_playlist_splitter.py', audio_file, args.txt_file], check=True)

# Run metadata_buster_edit_me.py
command = ['python3', 'metadata_buster_edit_me.py']

if args.approve:
    command.append('-a')
if args.folder:
    command.append('-f')
if args.directory:
    command.extend(['-d', args.directory])

subprocess.run(command, check=True)
