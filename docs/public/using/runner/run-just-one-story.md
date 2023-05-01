---
title: Run one story in collection
---



If you have just one story in your collection,
you can run it directly by using .one().




example.story:

```yaml
Do thing:
  steps:
    - Do thing
```
engine.py:

```python
from hitchstory import BaseEngine
from code_that_does_things import *

class Engine(BaseEngine):
    def do_thing(self):
        pass
```

With code:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine


story = StoryCollection(Path(".").glob("*.story"), Engine()).one()

```






```python
story.play()
```

Will output:
```
RUNNING Do thing in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
```









!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/one-story.story">one-story.story
    storytests.</a>

