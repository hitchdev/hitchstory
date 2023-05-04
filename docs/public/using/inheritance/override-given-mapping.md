---
title: Story inheritance - given mapping preconditions overridden
---



Child stories can be based upon parent stories. Given
preconditions are overridden

In this example, the parent story has a browser type of
firefox which is overridden as chrome. 

If you use inherit_via=GivenProperty.OVERRIDE then
child stories with partial given preconditions in the
form of mappings will override parent given preconditions.


# Code Example



example.story:

```yaml
Login:
  given:
    url: /loginurl
    browser:
      type: firefox
      size: 1024x768
  steps:
  - Fill form:
      username: hello
      password: password
  - Click: login

Log in using chrome:
  based on: login
  given:
    browser:
      type: chrome
```
engine.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty
from strictyaml import Map, Int, Str, MapPattern, Optional


class Engine(BaseEngine):
    given_definition = GivenDefinition(
        url=GivenProperty(schema=Str()),
        browser=GivenProperty(
            schema=Map({"type": Str(), "size": Str()}),
            inherit_via=GivenProperty.OVERRIDE,
        ),
    )

    def set_up(self):
        print("use browser {0}".format(self.given["browser"]["type"]))
        print("browser size {0}".format(self.given["browser"]["size"]))
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
browser size 1024x768
visit /loginurl
with password
enter password
with username
enter hello
clicked on login
SUCCESS in 0.1 seconds.
```





## Child







```python
collection.named("Log in using chrome").play()
```

Will output:
```
RUNNING Log in using chrome in /path/to/working/example.story ... use browser chrome
browser size 1024x768
visit /loginurl
with password
enter password
with username
enter hello
clicked on login
SUCCESS in 0.1 seconds.
```










!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/inheritance-given-mapping.story">inheritance-given-mapping.story
    storytests.</a>

