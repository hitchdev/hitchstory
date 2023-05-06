---
title: Story that rewrites itself
---



These examples show how to build stories that rewrite themselves
from program output (in-test snapshot testing). This can be done
with 

```
self.current_step.rewrite("argument").to("new output")
```


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
            will output: old value
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




## Story is rewritten when rewrite=True is used







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


## Story remains unchanged when rewrite=False is used instead







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

