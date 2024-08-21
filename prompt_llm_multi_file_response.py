import expand_file_references
from main_decorator import main
from prompt_llm import prompt_llm
from expand_file_references import expand_file_references

def add_instruction(request):
    return f"""
when providing code for a file:
1. rewrite the whole file with the modifications
2. use the following format:
### File: `{{file}}`
```{{language}}
{{code}}
```
3. multiple files are allowed
4. no line numbers

request:
{request}
"""

@main
def prompt_llm_multi_file_response(request):
    return prompt_llm(expand_file_references(add_instruction(request)))
