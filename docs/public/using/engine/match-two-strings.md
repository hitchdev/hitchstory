---
title: Match two strings and show diff on failure
---



While you could use `assert expected == actual` to match
two strings in a story step, if you use `strings_match(expected, actual)`
instead then when it fails:

* It will show the actual string, expected string *and a diff*.
* It will raise a Failure exception and avoid polluting the error message with the full stacktrace.

An example is shown below:


# Example



example.story:

```yaml
Failing story:
  steps:
    - Pass because strings match
    - Fail because strings don't match
```
engine.py:

```python
from hitchstory import BaseEngine, strings_match

class Engine(BaseEngine):
    def pass_because_strings_match(self):
        strings_match("hello", "hello")

    def fail_because_strings_dont_match(self):
        strings_match("hello", "goodbye")
```

With code:

```python
from hitchstory import StoryCollection
from engine import Engine
from pathlib import Path

story_collection = StoryCollection(Path(".").glob("*.story"), Engine())

```






```python
story_collection.one().play()
```

Will output:
```
RUNNING Failing story in /path/to/working/example.story ... FAILED in 0.1 seconds.

      steps:
      - Pass because strings match
      - Fail because strings don't match


hitchstory.exceptions.Failure

    Test failed.

ACTUAL:
goodbye

EXPECTED:
hello

DIFF:
- hello+ goodbye
```









!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/matching-strings.story">matching-strings.story
    storytests.</a>

