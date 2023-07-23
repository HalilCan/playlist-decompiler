
# Playlist Decompiler

`playlist_decompiler` is a Python script that automates the process of downloading a Youtube video, splitting it into tracks, and applying metadata to each track. This project consists of the main Python script (`playlist_decompiler.py`) and a series of helper scripts.

## Prerequisites

Before running Playlist Decompiler, make sure to install the following 
prerequisites:

- youtube-dl-nightly
- ffmpeg

## Scripts

This project consists of several scripts, each of which you can also use separately:

- `playlist_decompiler`: The main Python script that executes all tasks in sequence.
- `name_tilde_destroyer.sh`: A bash script that cleans up the filename of the downloaded audio file.
- `opus_to_m4a_converter.sh`: A bash script that converts the downloaded audio file to a format that's suitable for ffmpeg manipulations.
- `single_file_playlist_splitter.py`: A Python script that splits the audio file into tracks based on timestamps provided in a text file.
- `metadata_buster_edit_me.py`: A Python script that applies metadata to each track.

## Usage

To use Playlist Decompiler, run the `playlist_decompiler` script with the appropriate arguments:

```bash
python playlist_decompiler.py [-h] [-a] [-f] [-d DIRECTORY] txt_file video_url`
```

- `txt_file`: Path to the text file with timestamps and song names.
video_url: URL of the video to download.
- `-a, --approve`: Approve each metadata change. Typing $f instead of the new title, if you are asked, is a shorthand for making the title the filename.
- `-f, --folder`: Use the last folder's name as the artist name.
- `-d DIRECTORY, --directory DIRECTORY`: Specify the directory containing the files. By default, it's the current working directory.
- `-h`: Optional. Displays the help text.

## Contributing

Contributions are welcome! Please open an issue if you encounter any problems or have suggestions for improvements.

## License

This project is open-source and available under the MIT License.