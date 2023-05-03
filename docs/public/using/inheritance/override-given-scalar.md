---
title: Story inheritance - override given scalar preconditions
---



Child stories can be based upon parent stories.

If you change one precondition in a child story,
when it is run the steps and the other preconditions
will all remain the same.

In the following example the given url is changed from
/loginurl to /alternativeloginurl and the browser
remains as firefox.


# Example



example.story:

```yaml
Login:
  given:
    url: /loginurl
    browser: firefox
  steps:
  - Fill form:
      username: hello
      password: password
  - Click: login

Log in on alternate url:
  based on: login
  given:
    url: /alternativeloginurl
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
enter password
with username
enter hello
clicked on login
SUCCESS in 0.1 seconds.
```





## Child







```python
collection.named("Login").play()
```

Will output:
```
RUNNING Login in /path/to/working/example.story ... use browser firefox
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
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/inheritance-given-scalar.story">inheritance-given-scalar.story
    storytests.</a>

