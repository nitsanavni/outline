show the convo outside the code blocks

chat with llm remains visible
parts from it can be automatically used
e.g. shell commands can be run
named files code blocks can be

1. immediately "approved" -> copied to the target file
2. "show as diff" -> show the diff (.typistrc config "show as diff by default: true")

`typist exec git status`

prompt iteration workflow

cost estimation

## migrate us to lua

- [ ] R&D python-lua interop

`@main` decorator - where else is this relevant?
`@verify`

- we could support diffing parts of files
  - could be cool
  - similar to inline approvals

# typist

Core

change_requests to be a json file to support multiline change requests

Functionality

- `@file.def` - add a function to the context
- refactorings
  - move to file
  - rename
- "try harder" / "h" - use gpt-4o
- recipes: e.g. lift up conditional
  - could do it by recording recent changes
  - wrapper could be simple template or could be llm'ed
- approval process for multi-file changes
- can prompt return selection range?

UI

- vscode extension

Context Management

- `@test` - include test results
- support variables `$var`
- stateful context
- vars should be multi-line, especially the custom instructions - mayeb in files

Allow us to create a new file, not only change existing one

Need to think about multi file handling

Try to go with the natural way the LLM likes to format its responses

Git hook on commit suggesting message based on history and on the requested change

Teach mode, learn new skill

Keep conversation history

Connect a voice

Context can contain previous approved diffs

Showcase a 'no hands' session

Auto commit on green

# change one thing gpt

- ~~given a file and a change to make, output the changed code~~
- ~~from there we could wrap in a loop, showing diffs, running tests, approve,~~ commit,

- look into rope codeassist
- extract variable cli: support defining the range with `starts_on_line: int` + `starts_with: str`, `ends_on_line: int` + `ends_with: str`
  - add line numbers to the code given to the LLM
  - is it convenient for the LLM?
    - get gilded rose in here
  - maybe llms prefer writing regexes
- user request -> user shown a diff to approve with test results
- register a test
- replace vs. refactor
- do the todo
- [initial conversation with chat gpt](https://chat.openai.com/share/9390b11a-1e71-4821-9fd0-714da658f139)
- install Aider
- a chat script
- multi roots - each gets equal real estate in the output
