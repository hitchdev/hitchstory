---
title: Story with parameters
---



Parameterized stories are used to describe stories
which are essentially the same except for one or more
variables which can vary.

A common example is a story for a user to log in with
a browser which may be done with a number of different
browsers.

Parameters can be used in preconditions and in steps
by surrounding the parameter name with (( brackets )).




example.story:

```yaml
Click magic button:
  with:
    browser:
      name: firefox
      version: 37
  given:
    browser: (( browser ))
  steps:
  - Click on button
  - Save screenshot:
      for browser: (( browser ))

  variations:
    with chrome:
      with:
        browser:
          name: chrome
          version: 153
```
engine.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty, validate
from strictyaml import Map, Seq, Int, Str, Optional
from code_that_does_things import *

class Engine(BaseEngine):
    given_definition=GivenDefinition(
        browser=GivenProperty(
            schema=Map({"name": Str(), "version": Int()}),
            inherit_via=GivenProperty.OVERRIDE,
        ),
    )

    def set_up(self):
        print(self.given['browser']['name'])
        print(self.given['browser']['version'])

    def click_on_button(self):
        print("clicked!")

    @validate(for_browser=Map({"name": Str(), "version": Int()}))
    def save_screenshot(self, for_browser):
        print('save screenshot:')
        print("screenshot-{0}-{1}.png".format(
            for_browser['name'],
            for_browser['version']
        ))
```

With code:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine

story_collection = StoryCollection(Path(".").glob("*.story"), Engine())

```




## Default







```python
story_collection.named("Click magic button").play()

```

Will output:
```
RUNNING Click magic button in /path/to/working/example.story ... firefox
37
clicked!
save screenshot:
screenshot-firefox-37.png
SUCCESS in 0.1 seconds.
```





## Variation







```python
story_collection.named("Click magic button/with chrome").play()

```

Will output:
```
RUNNING Click magic button/with chrome in /path/to/working/example.story ... chrome
153
clicked!
save screenshot:
screenshot-chrome-153.png
SUCCESS in 0.1 seconds.
```





## Specify parameters with code







```python
story_collection.with_params(browser={"name": "ie", "version": "6"}).named("Click magic button").play()

```

Will output:
```
RUNNING Click magic button in /path/to/working/example.story ... ie
6
clicked!
save screenshot:
screenshot-ie-6.png
SUCCESS in 0.1 seconds.
```










!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/parameterization.story">parameterization.story
    storytests.</a>

