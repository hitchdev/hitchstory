
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
    - Failing step without stacktrace

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



```python
from hitchstory import StoryCollection
from engine import Engine
from pathquery import pathquery

story_collection = StoryCollection(pathquery(".").ext("story"), Engine())

```






```python
story_collection.one().play()
```

Will output:
```
RUNNING Failing story in /path/to/example.story ... FAILED in 0.1 seconds.

    Failing story:
      steps:
      - Failing step without stacktrace


code_that_does_things.ExampleException

    This is a demonstration exception docstring.

    It spreads across multiple lines.

Expected exception
```










!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/expected-exceptions.story">expected-exceptions.story
    storytests.</a>

