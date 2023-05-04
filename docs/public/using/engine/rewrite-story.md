---
title: Story that rewrites itself
---



Unlike every other integration testing framework, Hitch stories
can be rewritten according to the actual output of a program.

This lets you do rewrite acceptance test driven development (RATDD)
- where you change the code, autoregenerate the story and visually
inspect the new story to ensure it is correct.

This example shows a story being run in "rewrite" mode (where
rewrite=True) is fed to the engine and in normal mode.


# Code Example



example.story:

```yaml
Append text to file:
  steps:
    - Run: echo hello >> mytext.txt
    - Run: echo hello >> mytext.txt
    - Run: echo hello >> mytext.txt

  variations:
    Output text to:
      following steps:
        - Run and get output:
            command: cat mytext.txt
            will output: 
```
engine.py:

```python
from hitchstory import BaseEngine

class Engine(BaseEngine):
    def __init__(self, rewrite=True):
        self._rewrite = rewrite
    
    def run(self, command):
        pass

    def run_and_get_output(self, command, will_output):
        if self._rewrite:
            self.current_step.rewrite("will_output").to("hello\nhello")
```

With code:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine

```




## Rewritten







```python
StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).ordered_by_name().play()

```

Will output:
```
RUNNING Append text to file in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
RUNNING Append text to file/Output text to in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
```




File example.story should now contain:

```
Append text to file:
  steps:
  - Run: echo hello >> mytext.txt
  - Run: echo hello >> mytext.txt
  - Run: echo hello >> mytext.txt

  variations:
    Output text to:
      following steps:
      - Run and get output:
          command: cat mytext.txt
          will output: |-
            hello
            hello
```


## No changes







```python
StoryCollection(Path(".").glob("*.story"), Engine(rewrite=False)).ordered_by_name().play()

```

Will output:
```
RUNNING Append text to file in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
RUNNING Append text to file/Output text to in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
```




Then the example story will be unchanged.







!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/rewrite-story.story">rewrite-story.story
    storytests.</a>

