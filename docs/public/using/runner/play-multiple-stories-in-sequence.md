---
title: Play multiple stories in sequence
---



Running multiple stories in sequence is necessary when
you want to do a regression sweep to make sure nothing
has broken.

By default hitchstory will stop when it sees its first
failure. This behavior can be changed though.


# Code Example



base.story:

```yaml
Base story:
  given:
    random variable: some value
```
example1.story:

```yaml
Create file:
  based on: base story
  steps:
    - Create file
Create file again:
  based on: base story
  steps:
    - Create file
```
example2.story:

```yaml
Create files:
  based on: base story
  steps:
    - Create file
```

With code:

```python
from hitchstory import StoryCollection, BaseEngine, GivenDefinition, GivenProperty
from pathlib import Path
from ensure import Ensure

class Engine(BaseEngine):
    given_definition=GivenDefinition(
        random_variable=GivenProperty()
    )

    def create_file(self, filename="step1.txt", content="example"):
        with open(filename, 'w') as handle:
            handle.write(content)

```




## Running all stories in file order







```python
results = StoryCollection(
    [
        "base.story",
        "example1.story",
        "example2.story",
    ],
    Engine()
).ordered_by_file().play()
Ensure(results.all_passed).is_true()

```

Will output:
```
RUNNING Base story in /path/to/working/base.story ... SUCCESS in 0.1 seconds.
RUNNING Create file in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
RUNNING Create file again in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
RUNNING Create files in /path/to/working/example2.story ... SUCCESS in 0.1 seconds.
```





## Running all tests ordered by name in 'example1.story'







```python
StoryCollection(
    Path(".").glob("*.story"), Engine()
).in_filename("example1.story").ordered_by_name().play()

```

Will output:
```
RUNNING Create file in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
RUNNING Create file again in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
```





## Using .one() on a group of stories will fail







```python
StoryCollection(Path(".").glob("*.story"), Engine()).one()

```









!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/multiple.story">multiple.story
    storytests.</a>

