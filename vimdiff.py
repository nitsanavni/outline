import os

def vimdiff(file1, file2):
    os.system(f"diff -b {file1} {file2} || vimdiff {file1} {file2}")
