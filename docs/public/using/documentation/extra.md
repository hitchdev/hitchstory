---
title: Generate documentation with extra variables and functions
---


!!! warning "Experimental"

    This feature is in alpha. The API may change on a minor version increment.




Using extra=, you can use additional functions and variables
defined outside of the template.




example.story:

```yaml
Login:
  about: Simple log in.
  jiras: AZT-344, AZT-345
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
  - Drag:
      from item: left
      to item: right
  - Click:
      item: right
      double: yes


Log in on another url:
  about: Alternate log in URL.
  jiras: AZT-344, AZT-589
  based on: login
  given:
    url: /alternativeloginurl

Log in as president:
  about: For stories that involve Trump.
  jiras: AZT-611
  based on: login
  with:
    username: DonaldTrump
    password: iamsosmrt
```
engine.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty
from hitchstory import InfoDefinition, InfoProperty, validate
from strictyaml import Map, Int, Str, Bool, Optional, CommaSeparated


class Engine(BaseEngine):
    given_definition = GivenDefinition(
        url=GivenProperty(schema=Str()),
    )
    
    info_definition = InfoDefinition(
        jiras=InfoProperty(schema=CommaSeparated(Str())),
    )

    def set_up(self):
        print("visit {0}".format(self.given['url']))

    def fill_form(self, **textboxes):
        for name, text in sorted(textboxes.items()):
            print("with {0}".format(name))
            print("enter {0}".format(text))
      
    def drag(self, from_item, to_item):
        print(f"drag {from_item} to {to_item}")

    @validate(double=Bool())
    def click(self, item, double=False):
        if double:
            print(f"double clicked on {item}")
        else:
            print(f"clicked on {item}")
```
index.jinja2:

```yaml
{% for story in story_list %}
{{ story.documentation() }}
{% endfor %}
```
document.yaml:

```yaml
story: |
  # {{ name }}
  
  URL : {{ WEBSITE }}/stories/{{ slug }}.html
  
  {{ info.jiras.documentation() }}

  {{ about }}
info:
  jiras: |
    {% for jira in jiras -%}
    * {{ jira_url(jira) }}
    {% endfor %}
```

With code:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine
from path import Path
import jinja2

jenv = jinja2.Environment(
    undefined=jinja2.StrictUndefined, loader=jinja2.BaseLoader
)

story_collection = StoryCollection(
    Path(".").glob("*.story"), Engine()
).non_variations()

```






```python
extra = {
    "WEBSITE": "http://www.yourdocumentation.com/",
    "jira_url": lambda jira: f"https://yourproject.jira.com/JIRAS/{jira}",
}

print(
    jenv.from_string(Path("index.jinja2").text()).render(
        story_list=story_collection.with_documentation(
            Path("document.yaml").text(), extra=extra
        ).ordered_by_file()
    )
)

```

Will output:
```
# Login

URL : http://www.yourdocumentation.com//stories/login.html

* https://yourproject.jira.com/JIRAS/AZT-344
* https://yourproject.jira.com/JIRAS/AZT-345


Simple log in.

# Log in on another url

URL : http://www.yourdocumentation.com//stories/log-in-on-another-url.html

* https://yourproject.jira.com/JIRAS/AZT-344
* https://yourproject.jira.com/JIRAS/AZT-589


Alternate log in URL.

# Log in as president

URL : http://www.yourdocumentation.com//stories/log-in-as-president.html

* https://yourproject.jira.com/JIRAS/AZT-611


For stories that involve Trump.
```









!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/documentation-extra-vars-and-functions.story">documentation-extra-vars-and-functions.story
    storytests.</a>

