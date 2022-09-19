---
title: Continue on failure when playing multiple stories
---



By default whenever stories are played in sequence,
they stop when the first failure is encountered.

However, if your stories take a long time to run
you may wish to continue after the first failure.






example1.story:

```yaml
A Create file:
  steps:
  - Create file
B Create file:
  steps:
  - Fail

```


example2.story:

```yaml
C Create file a third time:
  steps:
    - Create file

```








```python
from hitchstory import StoryCollection, BaseEngine
from pathquery import pathquery


class Engine(BaseEngine):
    def create_file(self, filename="step1.txt", content="example"):
        with open(filename, 'w') as handle:
            handle.write(content)

    def fail(self):
        raise Exception("Error")

```




Stop on failure is default behavior:




```python
StoryCollection(
    pathquery(".").ext("story"), Engine()
).ordered_by_name().play()

```

Will output:
```
RUNNING A Create file in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
RUNNING B Create file in /path/to/working/example1.story ... FAILED in 0.1 seconds.

    B Create file:
      steps:
      - Fail


[1]: function 'fail'
  /path/to/working/examplepythoncode.py


        59 :
        60 :             def fail(self):
    --> 61 :                 raise Exception("Error")
        62 :



builtins.Exception
  Common base class for all non-exit exceptions.
Error
```






Continue on failure:




```python
StoryCollection(
    pathquery(".").ext("story"), Engine()
).ordered_by_name().continue_on_failure().play()

```

Will output:
```
RUNNING A Create file in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
RUNNING B Create file in /path/to/working/example1.story ... FAILED in 0.1 seconds.

    B Create file:
      steps:
      - Fail


[1]: function 'fail'
  /path/to/working/examplepythoncode.py


        59 :
        60 :             def fail(self):
    --> 61 :                 raise Exception("Error")
        62 :



builtins.Exception
  Common base class for all non-exit exceptions.
Error
RUNNING C Create file a third time in /path/to/working/example2.story ... SUCCESS in 0.1 seconds.
```











!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/fail-fast.story">fail-fast.story
    storytests.</a>

