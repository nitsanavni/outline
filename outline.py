import argparse
import os
import re

# Top-level dictionary for scoring
SCORING = {
    "class": 3,
    "def": 2,
    "__init__": 1,
    "__main__": 1,
    "if": 1,
    "else": 1,
    "elif": 1,
    "for": 1,
    "with": 1,
    "return": 1,
}


class Outline:
    def __init__(self, root_nodes=["."], max_lines=10, scoring=None):
        self.root_nodes = root_nodes
        self.outline = []
        self.scores = scoring if scoring else {}
        self.max_lines = max_lines

    def traverse(self, node=None):
        if not node:
            node = self.root_node
        if isinstance(node, list):
            for n in node:
                self.traverse(n)
        else:
            if os.path.isdir(node):
                for dirpath, dirnames, files in os.walk(node):
                    files = [f for f in files if not f[0] == "."]
                    dirnames[:] = [d for d in dirnames if not d[0] == "."]
                    for name in files:
                        file_path = os.path.join(dirpath, name)
                        if not self.is_binary(file_path):
                            self.parse_file(file_path)
            elif os.path.isfile(node):
                self.parse_file(node)
            else:
                print(f"Path '{node}' does not exist.")

    def is_binary(self, filename):
        try:
            with open(filename, "rb") as file:
                return any(byte > 127 for byte in file.read(1024))
        except (IOError, OSError):
            return False

    def parse_file(self, filename):
        try:
            with open(filename, "r", encoding="utf8", errors="ignore") as file:
                self.outline.append((filename, 100, len(self.outline), ""))
                for line_number, line in enumerate(file, 1):
                    stripped_line = line.strip("\n")
                    if not stripped_line.strip():  # Skip empty lines
                        continue
                    score = self.score_line(line)
                    self.outline.append(
                        (stripped_line, score, len(self.outline), line_number)
                    )
        except Exception as e:
            print(f"Error reading file {filename}: {e}")

    def score_line(self, line):
        score = 0
        indentation_level = len(line) - len(line.lstrip())
        score -= indentation_level

        for keyword, value in self.scores.items():
            if re.search(r"\b" + keyword + r"\b", line):
                score += value
        return score

    def summarize(self):
        for root_node in self.root_nodes:
            self.outline = []
            self.root_node = root_node
            self.traverse()

            self.outline.sort(key=lambda x: -x[1])
            summary = self.outline[: self.max_lines]
            summary.sort(key=lambda x: x[2])

            for line, score, position, line_number in summary:
                print(f"{line_number}:{line}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate codebase summary with Outline."
    )

    parser.add_argument(
        "-r",
        "--root",
        nargs="+",
        default=["."],
        help="The root directories to summarize. Default is the current directory.",
    )
    parser.add_argument(
        "-l",
        "--lines",
        type=int,
        default=10,
        help="The maximum number of output lines. Default is 10.",
    )

    args = parser.parse_args()

    outline = Outline(root_nodes=args.root, max_lines=args.lines, scoring=SCORING)
    outline.summarize()
