# change one thing gpt

- given a file and a change to make, output the changed code
- from there we could wrap in a loop, showing diffs, running tests, approve, commit,

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
