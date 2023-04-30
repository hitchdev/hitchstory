---
title: Match two strings
---



Where two strings should match you can use
should_match(expected, actual) to compare them.

If they don't match, a Failure exception with
the expected, actual and a diff between the two
will be printed for debugging purposes.

This makes it slightly more helpful than
assert expected == actual.




example.story:

```yaml
Failing story:
  steps:
    - Fail because strings don't match
```
engine.py:

```python
from hitchstory import BaseEngine, no_stacktrace_for, Failure, strings_match
from code_that_does_things import raise_example_exception, output, ExampleException

class Engine(BaseEngine):
    def passing_step(self):
        pass

    def failing_step(self):
        raise_example_exception("Towel not located")

    @no_stacktrace_for(ExampleException)
    def failing_step_without_stacktrace(self):
        raise_example_exception("Expected exception")

    def raise_special_failure_exception(self):
        raise Failure("Special failure exception - no stacktrace printed!")

    def fail_because_strings_dont_match(self):
        strings_match("hello", "hello")   # matching
        strings_match("hello", "goodbye") # nonmatching
        
    def step_that_will_not_run(self):
        pass
        
    def on_failure(self, result):
        pass

    def not_executed_step(self):
        pass
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

    Failing story:
      steps:
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

