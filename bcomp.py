import os

def bcomp(file1, file2):
    # only show diff if files are different
    os.system(f"diff -b {file1} {file2} || bcomp {file1} {file2}")
