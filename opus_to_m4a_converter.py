import os
import subprocess

# get the list of all files in directory
file_list = os.listdir()

for file in file_list:
    if file.endswith('.opus'):
        new_name = file.rsplit('.', 1)[0] + '.m4a'
        subprocess.run(['ffmpeg', '-i', file, '-c:a', 'aac', new_name], check=True)
        os.remove(file)
