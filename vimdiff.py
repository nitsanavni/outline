import os

def vimdiff(file1, file2):
    os.system(f"vimdiff {file1} {file2}")
