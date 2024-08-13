# typist

Core

- Move state to files
  - Files go under '.typist'
- Move out of internal prompt loop to cli commands
- register an auto-formatter

Functionality

- "try harder" / "h" - use gpt-4o
- allow running the tests anytime
- recipes: e.g. lift up conditional
  - could do it by recording recent changes
  - wrapper could be simple template or could be llm'ed
- run the tests after approval

UI

- better prompt
  - i - continue from existing instructions
- vscode extension

Context Management

- file ref: `@file#L3-14`
  - `@` - trigger `fzf`
  - `#L` - select line range
  - parser / template formatting - unwrap file refs
- support variables `$var`
- stateful context
- `@file#O20` - outlined file, numbers of lines is 20
- vars should be multi-line, especially the custom instructions - mayeb in files
  - use a better prompt, see ideas in `prompt.py`

Rebrand to Typist

Find a nice cli diff tool

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
