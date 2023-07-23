import subprocess
import argparse
import os
import shutil

# Check which Python interpreter is available
python_command = 'python3' if shutil.which('python3') else 'python'

# Create the argument parser for this script
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--approve", help="approve each metadata change. typing $f instead of the new title, if you are asked, is a shorthand for making the title the filename.", action="store_true")
parser.add_argument("-f", "--folder", help="use the last folder's name as the artist name", action="store_true")
parser.add_argument("-d", "--directory", help="specify the directory containing the files. DEFAULT is this file's directory", type=str, default=os.getcwd())
parser.add_argument("txt_file", help='path to the text file with timestamps and song names.')
parser.add_argument("video_url", help="URL of the video to download.")
args = parser.parse_args()

# Format the title to create filename (replace unallowed characters)
video_title = "downloaded_playlist"
audio_file = f"{video_title}.m4a"

try:
    # Download video
    subprocess.run(['youtube-dl-nightly', '-o', f"{video_title}.%(ext)s", 'bestaudio[ext=m4a]/bestaudio/best', '--extract-audio', '--audio-quality', '0', '--xattrs', '--ignore-errors', args.video_url])
except subprocess.CalledProcessError as e:
    print(f'Error occurred while running youtube-dl-nightly: {e}')
    print(f'Command: {e.cmd}')
    print(f'Exit status: {e.returncode}')
    print(f'Command output: {e.output}')


# Run the name_tilde_destroyer.py to clean up the file name.
subprocess.run([python_command, 'name_tilde_destroyer.py'], check=True)

# Run the opus_to_m4a_converter.py to convert for ffmpeg manipulations.
subprocess.run([python_command, 'opus_to_m4a_converter.py'], check=True)

# Run single_file_playlist_splitter.py
subprocess.run([python_command, 'single_file_playlist_splitter.py', audio_file, args.txt_file], check=True)

# Compose command for and run metadata_buster_edit_me.py
command = [python_command, 'metadata_buster_edit_me.py']

if args.approve:
    command.append('-a')
if args.folder:
    command.append('-f')
if args.directory:
    command.extend(['-d', args.directory])

subprocess.run(command, check=True)
