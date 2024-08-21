import sys
import tempfile

from parse_multiple_files_in_markdown import parse_markdown
from bcomp import bcomp

def touch(filename):
    with open(filename, "w"):
        pass

def multi_file_diffs(files, diff):
    for filename, contents in files:
        received_tmp = tempfile.NamedTemporaryFile(delete=False)
        received_tmp.write(contents.encode())
        received_tmp.close()

        touch(filename)

        diff(received_tmp.name, filename)


if __name__ == "__main__":
    md = sys.stdin.read()
    files = parse_markdown(md)

    multi_file_diffs(files, diff=bcomp)
