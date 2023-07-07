import os
import re


class Outline:
    def __init__(self, root_node='.', max_lines=10):
        self.root_node = root_node
        self.max_lines = max_lines
        self.scores = {'class': 1, 'def': 1, '__init__': 1}

    def traverse(self, node=None):
        if not node:
            node = self.root_node
        if os.path.isdir(node):
            for dirpath, dirnames, files in os.walk(node):
                # Remove hidden files and directories
                files = [f for f in files if not f[0] == '.']
                dirnames[:] = [d for d in dirnames if not d[0] == '.']

                for name in files:
                    if not self.is_binary(f"{dirpath}/{name}"):
                        self.parse_file(os.path.join(dirpath, name))
        elif os.path.isfile(node):
            self.parse_file(node)
        else:
            print(f"Path '{node}' does not exist.")

    def is_binary(self, filename):
        """
        Return true if the file is binary.
        """
        try:
            with open(filename, 'rb') as file:
                for num in range(49152):
                    byte = file.read(1)
                    if byte == b"":
                        break
                    if byte > b"\x7f":
                        return True
        except (IOError, OSError):
            pass
        return False

    def parse_file(self, filename):
        with open(filename, 'rb') as file:
            print(f"{filename}:")
            for line in file:
                line = line.decode('utf8', 'ignore')
                print(f"{line}:{self.score_line(line)}")

    def score_line(self, line):
        score = 0
        for keyword, value in self.scores.items():
            if re.search(r'\b' + keyword + r'\b', line):
                score += value
        return score

    def summarize(self):
        self.traverse()
        # TODO: limit and format output here


if __name__ == "__main__":
    outline = Outline()
    outline.summarize()
