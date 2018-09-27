---
title: Set up with HitchKey
---

You can quickstart hitchstory with hitchkey by installing the hitchkey bootstrapper with [pipsi](https://github.com/mitsuhiko/pipsi):

```bash
pipsi install hitchkey
```

Or, if you don't want to install pipsi, this is also safe and won't affect any system dependencies:

```bash
sudo pip install hitchkey
```

In your project, create a "hitch" directory and drop the following files in it:

mystory.story, containing a story with one step:

```yaml
My first story:
  steps:
  - Do something
```

engine.py, containing code that executes stories but doesn't do anything:

```
from hitchstory import BaseEngine

class Engine(BaseEngine):
    def __init__(self, paths):
        self.path = paths

    def set_up(self):
        pass

    def do_something(self):
        pass
```

key.py, containing code to run stories:

```
from hitchstory import exceptions, StoryCollection
from pathquery import pathquery
from engine import Engine
from hitchrun import DIR, expected

@expected(exceptions.HitchStoryException)
def bdd(*keywords):
    """
    Run story with name containing keywords.
    """
    StoryCollection(pathquery(DIR.key).ext("story"), Engine(DIR)).shortcut(*keywords).play()


@expected(exceptions.HitchStoryException)
def regression():
    """
    Run all stories
    """
    StoryCollection(pathquery(DIR.key).ext("story"), Engine(DIR)).ordered_by_name().play()
```

hitchreqs.in, containing all the python packages you want installed in the virtualenv used by key.py and engine.py:

```
hitchstory
pathquery
hitchrun
```

Then, you can enter *any* directory in your project and run:

```bash
hk bdd my
```

And you should get a lot of virtualenv set up followed by:

```
RUNNING My first story in /path/to/mystory.story ... SUCCESS in 0.0 seconds.
```

Then, if you run it again with a ready virtualenv it should be quicker:

```
RUNNING My first story in /path/to/mystory.story ... SUCCESS in 0.0 seconds.
```

