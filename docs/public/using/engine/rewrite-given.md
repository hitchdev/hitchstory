---
title: Story that rewrites given preconditions
---



These examples show how to build stories that rewrite their given
preconditions from program output.

This is useful for auto-updating given preconditions when the
outside world changes. For example, if a a REST API service that
is being mocked starts returning different data you can
run the story in rewrite mode to update the mock.

The command to perform this rewrite is:

```
self.current_step.rewrite("argument").to("new output")
```

Note that if there is a story inheritance hierarchy then only the
child story's given preconditions will be updated.


# Code Example



example1.story:

```yaml
Basic:
  given:
    mock api:
      request: |
        {"greeting": "hello"}
      response: |
        {"greeting": "hi"}
  steps:
    - Call API
```
example2.story:

```yaml
Overridden response:
  based on: basic
  given:
    mock api:
      response: |
        {"greeting": "bonjour"}
```
example3.story:

```yaml
Overridden request:
  based on: basic
  given:
    mock api:
      request: |
        {"greeting": "hi there"}
```
example4.story:

```yaml
Story with variations:
  steps:
  - Call API

  variations:
    French:
      given:
        mock api:
          response: |
            {"greeting": "bonjour"}

    Chinese:
      given:
        mock api:
          request: |
            {"greeting": "Ni hao"}
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
            self.given.rewrite("Mock API", "response").to("""{"greeting": "bye"}\n""")
```

With code:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine

```




## Simple







```python
StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).named("Basic").play()

```

Will output:
```
RUNNING Basic in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
```




File example1.story should now contain:

```
Basic:
  given:
    mock api:
      request: |
        {"greeting": "hello"}
      response: |
        {"greeting": "bye"}
  steps:
  - Call API
```


## Overridden response







```python
StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).named("Overridden response").play()

```

Will output:
```
RUNNING Overridden response in /path/to/working/example2.story ... SUCCESS in 0.1 seconds.
```




File example2.story should now contain:

```
Overridden response:
  based on: basic
  given:
    mock api:
      response: |
        {"greeting": "bye"}
```


## Overridden request







```python
StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).named("Overridden request").play()

```

Will output:
```
RUNNING Overridden request in /path/to/working/example3.story ... SUCCESS in 0.1 seconds.
```




File example3.story should now contain:

```
Overridden request:
  based on: basic
  given:
    mock api:
      request: |
        {"greeting": "hi there"}
      response: |
        {"greeting": "bye"}
```


## Story with variations







```python
StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).named("Story with variations/French").play()

```

Will output:
```
RUNNING Story with variations/French in /path/to/working/example4.story ... SUCCESS in 0.1 seconds.
```




File example4.story should now contain:

```
Story with variations:
  steps:
  - Call API

  variations:
    French:
      given:
        mock api:
          response: |
            {"greeting": "bye"}

    Chinese:
      given:
        mock api:
          request: |
            {"greeting": "Ni hao"}
```







!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/rewrite-given.story">rewrite-given.story
    storytests.</a>

