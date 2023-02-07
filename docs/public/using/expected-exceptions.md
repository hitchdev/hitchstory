---
title: Hiding stacktraces for expected exceptions
---



For common expected failures where you do not want
to see the whole stacktrace, apply the "@no_stacktrace_for"
decorator.




example.story:

```yaml
Failing story:
  steps:
    - Passing step
    - Failing step
    - Not executed step
```
engine.py:

```python
from hitchstory import BaseEngine, no_stacktrace_for, Failure
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


example.story:

```yaml
Failing story:
  steps:
    - Failing step without stacktrace
```






```python
story_collection.one().play()
```

Will output:
```
RUNNING Failing story in /path/to/working/example.story ... FAILED in 0.1 seconds.

      steps:
      - Passing step
      - Failing step
      - Not executed step


[1]: function 'failing_step'
  /path/to/working/engine.py


        6 :
        7 :     def failing_step(self):
    --> 8 :         raise_example_exception("Towel not located")
        9 :



[2]: function 'raise_example_exception'
  /path/to/working/code_that_does_things.py


        21 :
        22 : def raise_example_exception(text=""):
    --> 23 :     raise ExampleException(text)
        24 :



code_that_does_things.ExampleException

    This is a demonstration exception docstring.

    It spreads across multiple lines.

Towel not located
```









!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/expected-exceptions.story">expected-exceptions.story
    storytests.</a>

