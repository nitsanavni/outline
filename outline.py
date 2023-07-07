import os
import re


class Outline:
    def __init__(self, root_node='.', max_lines=10):
        self.root_node = root_node
        self.max_lines = max_lines
        self.scores = {'class': 1, 'def': 1, '__init__': 1}
        self.outline = []

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
            # Add the file path to the outline with a high score
            # assuming file paths have a score of 100
            position = len(self.outline)
            self.outline.append((filename, 100, position))
            # print(f"{filename}:")
            for line in file:
                line = line.decode('utf8', 'ignore')
                position = len(self.outline)
                # print(f"{line}:{self.score_line(line)}")
                self.outline.append((line, self.score_line(line), position))

    def score_line(self, line):
        score = 0
        for keyword, value in self.scores.items():
            if re.search(r'\b' + keyword + r'\b', line):
                score += value
        return score

    def summarize(self):
        self.traverse()

        # Sort outline by scores in descending order
        self.outline.sort(key=lambda x: -x[1])

        # Select max_lines highest scored lines
        summary = self.outline[:self.max_lines]

        # this doesn't seem to sort by 'position'
        summary.sort(key=lambda x: x[2])

        # Format output
        for line, score, position in summary:
            print(f"Score: {score} Line: {line}")


if __name__ == "__main__":
    outline = Outline()
    outline.summarize()
