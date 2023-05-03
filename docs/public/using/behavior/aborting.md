---
title: Abort a story with ctrl-C
---



When an in-progress story is hit with any of the
following termination signals:

* SIGTERM
* SIGINT
* SIGQUIT
* SIGHUP

Then it triggers the tear_down method of the
engine.

In practical terms this means that if you are running
a series of stories, Ctrl-C should halt current execution,
run tear_down and then not run any more stories.


# Example



example.story:

```yaml
Create files:
  steps:
    - Pause forever

Should never run:
  steps:
    - Should not happen
```
engine.py:

```python
from hitchstory import BaseEngine
from code_that_does_things import reticulate_splines
import psutil

class Engine(BaseEngine):
    def pause_forever(self):
        psutil.Process().terminate()

    def should_not_happen(self):
        raise Exception("This exception should never be triggered")

    def tear_down(self):
        print("Reticulate splines")
```

With code:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine

```






```python
StoryCollection(Path(".").glob("*.story"), Engine()).ordered_by_name().play()
```

Will output:
```
RUNNING Create files in /path/to/working/example.story ... Aborted
Reticulate splines
```









!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/abort.story">abort.story
    storytests.</a>

