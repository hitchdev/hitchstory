---
title: Arguments to steps
---



Arguments are fed to steps in a way that is
largely consistent with how python methods work:

- Named arguments are put in equivalent slugified variables (e.g. "How many times" -> "how_many_times") - demonstrated in the click step below.
- If the method has **kwargs then the key names of kwargs will match the named arguments exactly - demonstrated in the fill_form step below.

@validate is used with [StrictYAML validators](../../../../strictyaml/using)
to validate the type of the steps. You can see more about this in
[strong typing](../strong-typing).




engine.py:

```python
from code_that_does_things import *
from strictyaml import Int, Str, Bool
from hitchstory import BaseEngine, validate

class Engine(BaseEngine):
    def fill_form(self, **kwargs):
        for name, content in kwargs.items():
            fill_form(name, content)

    @validate(what=Str(), how_many_times=Int(), double_click=Bool())
    def click(self, what, how_many_times=1, double_click=False):
        for _ in range(how_many_times):
            click(what)
```

With code:

```python
from hitchstory import StoryCollection
from engine import Engine
from pathlib import Path

```




## kwargs





example.story:

```yaml
Login:
  steps:
    - Fill form:
        login username: john
        login password: hunter2
```




```python
StoryCollection(Path(".").glob("*.story"), Engine()).named("Login").play()

```

Will output:
```
RUNNING Login in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
```




Then the form is filled with:


* login username: john

* login password: hunter2



## optional args single argument





example.story:

```yaml
Click button:
  steps:
    - Click: my button
```




```python
StoryCollection(Path(".").glob("*.story"), Engine()).named("Click button").play()

```

Will output:
```
RUNNING Click button in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
```





## optional args fewer than the maximum arguments





example.story:

```yaml
Click button:
  steps:
    - Click:
        what: my button
        how many times: 2
```




```python
StoryCollection(Path(".").glob("*.story"), Engine()).named("Click button").play()

```

Will output:
```
RUNNING Click button in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
```










!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/arguments.story">arguments.story
    storytests.</a>

