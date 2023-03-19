---
title: Story inheritance - parameters
---


!!! warning "Experimental"

    This feature is in alpha. The API may change on a minor version increment.




Child stories can be based upon parent stories.

Parameters will be overridden.

NOTE: This feature has a bug, avoid using.




example.story:

```yaml
Login:
  given:
    url: /loginurl
    browser: firefox
  with:
    username: AzureDiamond
    password: hunter2
  steps:
  - Fill form:
      username: (( username ))
      password: (( password ))
  - Click: login
  - Click: inbox

Visit inbox:
  based on: login
  with:
    username: DonaldTrump
    password: Th3Don@ld
```
engine.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty
from strictyaml import Map, Int, Str, MapPattern, Optional


class Engine(BaseEngine):
    given_definition = GivenDefinition(
        url=GivenProperty(schema=Str()),
        browser=GivenProperty(schema=Str()),
    )

    def set_up(self):
        print("use browser {0}".format(self.given["browser"]))
        print("visit {0}".format(self.given['url']))

    def fill_form(self, **textboxes):
        for name, text in sorted(textboxes.items()):
            print("with {0}".format(name))
            print("enter {0}".format(text))

    def click(self, item):
        print("clicked on {0}".format(item))
```

With code:

```python
from hitchstory import StoryCollection
from engine import Engine
from pathlib import Path

collection = StoryCollection(Path(".").glob("*.story"), Engine())

```




## Parent







```python
collection.named("Login").play()
```

Will output:
```
RUNNING Login in /path/to/working/example.story ... use browser firefox
visit /loginurl
with password
enter (( password ))
with username
enter (( username ))
clicked on login
clicked on inbox
SUCCESS in 0.1 seconds.
```





## Child







```python
collection.named("Visit inbox").play()
```

Will output:
```
RUNNING Visit inbox in /path/to/working/example.story ... use browser firefox
visit /loginurl
with password
enter (( password ))
with username
enter (( username ))
clicked on login
clicked on inbox
SUCCESS in 0.1 seconds.
```










!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/inheritance-parameters.story">inheritance-parameters.story
    storytests.</a>

