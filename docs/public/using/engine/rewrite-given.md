---
title: Story that rewrites given preconditions
---



These examples show how to build stories that rewrite themselves
from program output (in-test snapshot testing) but that rewrite
the given preconditions.

This is useful for changing

```
self.current_step.rewrite("argument").to("new output")
```


# Code Example



example.story:

```yaml
Call API:
  given:
    mock api:
      request: |
        {"greeting": "hello"}
      response: |
        {"greeting": "hi"}
  steps:
    - Call API
```
engine.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty
from strictyaml import Map, Str

class Engine(BaseEngine):
    given_definition = GivenDefinition(
        mock_api=GivenProperty(
            schema=Map({"request": Str(), "response": Str()}),
            inherit_via=GivenProperty.OVERRIDE,
        ),
    )

    def __init__(self, rewrite=True):
        self._rewrite = rewrite
    
    def call_api(self):
        if self._rewrite:
            self.given.rewrite("Mock API", "response").to("""{"greeting": "bye"}""")
```

With code:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine

```






```python
StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).ordered_by_name().play()

```

Will output:
```
RUNNING Call API in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
```




File example.story should now contain:

```
Call API:
  given:
    mock api:
      request: |
        {"greeting": "hello"}
      response: |
        {"greeting": "bye"}
  steps:
    - Call API
```






!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/rewrite-given.story">rewrite-given.story
    storytests.</a>

