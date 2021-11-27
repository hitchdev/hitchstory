
---
title: Given preconditions
type: using
---



Stories are comprised of preconditions followed by steps.

Hitchstory lets you define preconditions using the 'given' keyword
in YAML and then use them using self.given['property name'].

The given property names need to first be specified in the engine
using GivenDefinition and GivenProperty.

By default, given properties will parse
[without a StrictYAML schema](/strictyaml/using/alpha/howto/without-a-schema/),
but you can also specify your own [StrictYAML schema](https://hitchdev.com/strictyaml).

The following example shows a browser precondition being used to set up
a mock selenium object.




example.story:

```yaml
Load with chrome:
  given:
    browser configuration:
      name: chrome
      version: 22.0
      platform: linux
  steps:
  - Load website

Load with small firefox window:
  given:
    browser configuration:
      name: firefox
      platform: linux
      dimensions:
        height: 200
        width: 200
  steps:
  - Load website

```









engine.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty
from strictyaml import Optional, Str, Map, Enum, Seq, Int, MapPattern
from mockselenium import Webdriver

class Engine(BaseEngine):
    given_definition=GivenDefinition(
        browser_configuration=GivenProperty(
            schema=Map({
                "name": Str(),
                "platform": Enum(["linux", "osx", "windows"]),
                Optional("version"): Str(),
                Optional("dimensions"): Map({"height": Int(), "width": Int()}),
            })
        ),
    )

    def set_up(self):
        browser = self.given["browser configuration"]
        self.driver = Webdriver(
            name=browser['name'],
            platform=browser['platform'],
            version=browser.get('version'),
            dimensions=browser.get('dimensions', {"height": 1000, "width": 1000}),
        )

    def load_website(self):
        self.driver.visit("http://www.google.com")

```



```python
from hitchstory import StoryCollection
from pathquery import pathquery
from engine import Engine

```




Specified:




```python
StoryCollection(pathquery(".").ext("story"), Engine()).ordered_by_name().play()

```

Will output:
```
RUNNING Load with chrome in /path/to/example.story ...
Browser name: chrome
Platform: linux
Version: 22.0
Dimensions: 1000 x 1000

Visiting http://www.google.com
SUCCESS in 0.1 seconds.
RUNNING Load with small firefox window in /path/to/example.story ...
Browser name: firefox
Platform: linux
Dimensions: 200 x 200

Visiting http://www.google.com
SUCCESS in 0.1 seconds.
```










{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/given.story">given.story</a>.
{{< /note >}}
