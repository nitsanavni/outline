# Outline

Outline is a source code summarizer utility designed to provide a quick, high-level overview of your codebase. It generates a summary of your code as an outline by prioritizing file paths and selected lines of code (LOC) based on a scoring scheme. It's a useful tool for developers who want a quick overview of a large codebase, or to keep track of the main points of their own projects.

## How it works

Outline performs a breadth-first traversal over your codebase, starting from the provided root nodes. By default, the root node is the current directory.

The utility produces a summary with a maximum number of lines specified by the user. The default maximum is 10 lines.

The scoring scheme of Outline prioritizes file paths over LOC. Within LOC, lines that contain certain keywords (e.g., `class`) are scored higher. This behavior can be modified as needed through a configuration file.

## Configuration

Outline allows for a per-project or per-language configuration through an `.outlinerc.toml` file. The configuration file can specify different values for `max_lines`, `root_nodes`, and `regex_scores`, allowing for a high degree of customization.

Here is an example configuration:

```toml
[default]
max_lines = 20
root_nodes = ["./main", "./utils"]
regex_scores = ["class", "def", "__init__"]

[python]
max_lines = 15
regex_scores = ["class", "def", "__init__", "import"]

[javascript]
max_lines = 10
regex_scores = ["function", "import", "export", "class"]
```

In this configuration:

-   The `default` settings apply to all languages unless a specific language provides its own settings.
-   `max_lines` specifies the maximum number of output lines.
-   `root_nodes` are the root nodes to summarize. It's a list of paths.
-   `regex_scores` is a list of regex patterns to use for scoring lines of code. The first pattern in the list scores higher than the second, the second scores higher than the third, and so on.

## Usage

You can use Outline from the command line as follows:

```shell
$ python main.py -r <root_node_1> <root_node_2> ... -l <max_lines>
```

Where:

-   `-r` or `--root` are the root nodes to summarize. It accepts a list of paths. Default is the current directory ('.').
-   `-l` or `--lines` is the maximum number of output lines. Default is 10.

For example, to summarize the `./main` and `./utils` directories with up to 20 lines of output, use:

```shell
$ python main.py -r ./main ./utils -l 20
```

To use the defaults (current directory as the root node, 10 lines of output), simply use:

```shell
$ python main.py
```

## Tests

Tests are located in the `./test` directory. To run the tests, use:

```shell
$ python -m unittest discover -s test
```

## Contributing

Contributions to Outline are always welcome! Please refer to our [Contributing Guide](CONTRIBUTING.md) for more information.

## License

Outline is licensed under the [MIT license](LICENSE.txt).
