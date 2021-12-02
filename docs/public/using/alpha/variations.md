
---
title: Variations
---



Some stories are very similar except for a few changed items. You
can create substories within the same story in order to enumerate
all of the possible permutations.

This works in the same way as inheritance.




example.story:

```yaml
Create files:
  given:
    content: dog
    hierarchical content:
      x: 1
      y:
        - 42
  steps:
    - Do thing with precondition
    - Do other thing: dog
    - Do yet another thing
    - Do a fourth thing:
        animals:
          pond animal: frog
  variations:
    cat:
      given:
        content: cat

```












```python
from hitchstory import StoryCollection, BaseEngine, GivenDefinition, GivenProperty, validate
from strictyaml import Map, Seq, Int, Str, Optional
from pathquery import pathquery
from ensure import Ensure


class Engine(BaseEngine):
    given_definition=GivenDefinition(
        content=GivenProperty(schema=Str()),
        hierarchical_content=GivenProperty(
            schema=Map({"x": Int(), "y": Seq(Str())})
        ),
    )

    def do_other_thing(self, parameter):
        assert type(parameter) is str
        print(parameter)

    def do_thing_with_precondition(self):
        assert type(self.given['content']) is str
        print(self.given['content'])

    def do_yet_another_thing(self):
        assert type(self.given['hierarchical_content']['y'][0]) is str
        print(self.given['hierarchical_content']['y'][0])

    @validate(animals=Map({"pond animal": Str()}))
    def do_a_fourth_thing(self, animals=None):
        assert type(animals['pond animal']) is str
        print(animals['pond animal'])

story_collection = StoryCollection(pathquery(".").ext("story"), Engine())

```




Play:




```python
story_collection.shortcut("cat").play().report()

```

Will output:
```
RUNNING Create files/cat in /path/to/example.story ... cat
dog
42
frog
SUCCESS in 0.1 seconds.
```






Non-variations:




```python
Ensure([
    story.name for story in story_collection.non_variations().ordered_by_name()
]).equals(
    ["Create files", ]
)

```






Variations on story:




```python
Ensure([
    story.name for story in story_collection.named("Create files").variations
]).equals(
    ["Create files/cat"],
)

```






Only children:




```python
Ensure([
    story.name for story in story_collection.only_uninherited().ordered_by_name()
]).equals(
    ["Create files/cat"],
)

```











!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/variations.story">variations.story
    storytests.</a>

