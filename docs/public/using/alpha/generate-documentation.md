
---
title: Generate documentation from stories
---



hitchstory YAML stories *are* designed to be readable, but also terse
and easy to maintain.

Where terseness and ease of maintenance trumps readability, the former
take precedence. YAML stories are *not* intended to be a replacement for
stakeholder documentation in and of themselves.

YAML stories *are* designed, however, to be used to generate documentation
for use by stakeholders.

The example shown below demonstrates how a story can be transformed into
markdown via jinja2. This markdown can then be used to generate HTML
with a static site generator.




example.story:

```yaml
Login:
  about: Simple log in.
  with:
    username: AzureDiamond
    password: hunter2
  given:
    url: /loginurl
  steps:
  - Fill form:
      username: (( username ))
      password: (( password ))
  - Click: login


Log in on another url:
  about: Alternate log in URL.
  based on: login
  given:
    url: /alternativeloginurl

Log in as president:
  about: For stories that involve Trump.
  based on: login
  with:
    username: DonaldTrump
    password: iamsosmrt

```









engine.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty, about
from strictyaml import Map, Int, Str, Optional


class Engine(BaseEngine):
    given_definition = GivenDefinition(
        url=GivenProperty(schema=Str(), document="Load: {{ url }}"),
    )

    def set_up(self):
        print("visit {0}".format(self.given['url']))

    @about((
        "{% for name, value in textboxes.items() %}\n"
        "- Enter text '{{ value }}' in {{ name }}.\n"
        "{%- endfor %}\n"
    ))
    def fill_form(self, **textboxes):
        for name, text in sorted(textboxes.items()):
            print("with {0}".format(name))
            print("enter {0}".format(text))

    @about("* Click on {{ item }}")
    def click(self, item):
        print("clicked on {0}".format(item))

```



```python
from hitchstory import StoryCollection
from pathquery import pathquery
from engine import Engine
from path import Path
from jinja2 import Template

```




Generate from story:




```python
print(
    Template(Path("documentation.jinja2").text()).render(
        story_list=StoryCollection(
            pathquery(".").ext("story"), Engine()
        ).non_variations().ordered_by_file()
    )
)

```

Will output:
```
Login
-----

Simple log in.


Load: /loginurl



- Enter text 'AzureDiamond' in username.
- Enter text 'hunter2' in password.

* Click on login


Log in on another url
---------------------

Alternate log in URL.


Load: /alternativeloginurl



- Enter text 'AzureDiamond' in username.
- Enter text 'hunter2' in password.

* Click on login


Log in as president
-------------------

For stories that involve Trump.


Load: /loginurl



- Enter text 'DonaldTrump' in username.
- Enter text 'iamsosmrt' in password.

* Click on login
```











!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/documentation.story">documentation.story
    storytests.</a>

