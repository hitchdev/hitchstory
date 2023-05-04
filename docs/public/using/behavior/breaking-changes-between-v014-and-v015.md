---
title: Upgrade breaking changes between v0.14 and v0.15
---



Version 0.15 contains two important breaking changes:

* For every GivenProperty with a mapping schema inherit_via must be specified as either OVERRIDE or REPLACE.

* If parent stories have steps, child stories must specify either "replacement steps" or "following steps" instead of "steps".


# Code Example



example.story:

```yaml
Create files:
  given:
    browser:
      type: chrome
      size: 1024x768
  steps:
   - Add product:
      name: Towel
      quantity: 3
```

With code:

```python
from hitchstory import StoryCollection
from engine import Engine
from pathlib import Path

collection = StoryCollection(Path(".").glob("*.story"), Engine())

```




## GivenProperty with a mapping schema have inherit_via specified

In this example, inherit_via is not specified on GivenProperty.




engine.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty, validate
from strictyaml import Int, Map, Str

class Engine(BaseEngine):
    given_definition = GivenDefinition(
        browser=GivenProperty(
            schema=Map({"type": Str(), "size": Str()}),
        ),
    )

    @validate(quantity=Int())
    def add_product(self, name, quantity):
        pass
```




```python
collection.one().play()
```




## GivenProperty without a mapping schema must not have inherit_via specified

In this example, inherit_via is specified on a GivenProperty schema with an strictyaml Any schema specified. It would behave the same way if Seq(), Str()
or Int() or any other scalar validator were used.




engine.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty, validate
from strictyaml import Int, Map, Str, Any

class Engine(BaseEngine):
    given_definition = GivenDefinition(
        browser=GivenProperty(
            schema=Any(),
            inherit_via=GivenProperty.OVERRIDE,
        ),
    )

    @validate(quantity=Int())
    def add_product(self, name, quantity):
        pass
```




```python
collection.one().play()
```




## Using steps on child story where parent also has steps

In this example a parent story has steps and a child story
also has steps. Since this is ambiguous, this behavior
is disallowed since version 2.0.




example_child.story:

```yaml
Create other files:
  based on: create files
  steps:
  - Add product:
      name: Towel
      quantity: 3
```
engine.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty, validate
from strictyaml import Int, Map, Str

class Engine(BaseEngine):
    given_definition = GivenDefinition(
        browser=GivenProperty(
            schema=Map({"type": Str(), "size": Str()}),
            inherit_via=GivenProperty.OVERRIDE,
        ),
    )

    @validate(quantity=Int())
    def add_product(self, name, quantity):
        pass
```




```python
collection.named("Create other files").play()
```









!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/breaking-changes-between-v014-and-v015.story">breaking-changes-between-v014-and-v015.story
    storytests.</a>

