1. `main.py`: This is the main python script that will be run from the command line. This file will handle parsing command line arguments (root nodes, number of output lines), initiating the code traversal, and output the summary.

2. `config.py`: To handle the configuration settings from the `.outlinerc.toml` file. It should be able to parse the configuration, apply defaults and handle missing keys.

3. `scorer.py`: To prioritize score based on regex patterns and manage the overall scoring scheme.

4. `traverser.py`: To manage the breadth-first traversal of the codebase. It should be able to handle directory navigation all the way down to reading individual lines of code.

5. `summarizer.py`: To generate the summary by limiting the output to the maximum number of lines requested and displaying the pertinent information.

6. `test` directory: Path where unit tests live. Each of the above files (except `main.py`) should have a corresponding test file in this directory, such as `test_config.py`, `test_scorer.py`, etc.

7. `.outlinerc.toml` file: The configuration file. This won't need to be created in our implementation as it is project-specific.

Please note that the exact files and their functions may vary depending upon the specific implementation details.

Also, don't forget about the documentation files:

8. `README.md`: Explains what the program does, how to install and use it.

9. `Contributing.md`: Guidelines on how to contribute to the project.

10. `License.txt`: The license file.
