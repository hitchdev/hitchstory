---
title: Match two JSON snippets
---



While you could use `assert json.loads(expected) == json.loads(actual)` to match
two JSON in a story step, if you use `json_match(expected, actual)`
instead then when it fails:

* It will warn you if it failed because it wasn't valid JSON.
* It will show cleanly formatted actual JSON, expected JSON and a diff.
* It will raise a Failure exception and avoid polluting the error message with the full stacktrace.


# Example



example.story:

```yaml
Failing story:
  steps:
    - Pass because json matches
    - Fail because strings don't match
```
engine.py:

```python
from hitchstory import BaseEngine, json_match

class Engine(BaseEngine):
    def pass_because_json_matches(self):
        json_match(
            """{"a": 1, "b": 2}""",
            """{"b": 2, "a": 1}"""
        )

    def fail_because_strings_dont_match(self):
        json_match(
            """{"a": 1, "b": 2}""",
            """{"b": 2, "a": 1, "d": 3}"""
        )
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
      - Pass because json matches
      - Fail because strings don't match


hitchstory.exceptions.Failure

    Test failed.

ACTUAL:
{
    "a": 1,
    "b": 2,
    "d": 3
}

EXPECTED:
{
    "a": 1,
    "b": 2
}

DIFF:
  {
      "a": 1,
-     "b": 2
+     "b": 2,
?           +
+     "d": 3
  }
```









!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/matching-json.story">matching-json.story
    storytests.</a>

