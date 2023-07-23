import os

# get the list of all files in directory
file_list = os.listdir()

for file in file_list:
    base_name, extension = os.path.splitext(file)
    if '-' in base_name:
        new_name = base_name.rsplit('-', 1)[0] + extension
        os.rename(file, new_name)
