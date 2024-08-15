import ast
import sys


def get_function_code(file_path, function_name):
    with open(file_path, "r") as file:
        file_content = file.read()

    # Parse the file content into an AST
    parsed_ast = ast.parse(file_content)

    start_lineno = None
    end_lineno = None

    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            # Find the line number of the first decorator
            first_decorator_line = node.lineno
            for decorator in node.decorator_list:
                decorator_line = decorator.lineno
                if decorator_line < first_decorator_line:
                    first_decorator_line = decorator_line

            # Set the start and end line numbers
            start_lineno = first_decorator_line - 1
            end_lineno = node.body[-1].lineno

            # Extract the code lines
            lines = file_content.splitlines()[start_lineno:end_lineno]
            return "\n".join(lines)

    return None


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python print_def.py <file_path> <function_name>")
        sys.exit(1)

    file_path = sys.argv[1]
    function_name = sys.argv[2]

    function_code = get_function_code(file_path, function_name)

    if function_code:
        print(function_code)
    else:
        print(f"Function '{function_name}' not found in {file_path}.")
