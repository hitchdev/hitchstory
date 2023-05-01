---
title: Gradual typing of story steps
---



In order to speed up prototyping and development
of a story suite, the structure of your YAML data
specified in preconditions, parameters and step
arguments need not be strictly defined in advance.

All story data that is parsed without a validator
is parsed either as a dict, list or string.

It is nonetheless still recommended that you
apply validators as soon as possible.
[See more about that here](../strong-typing).




example.story:

```yaml
Create files:
  given:
    files created:
      preconditionfile.txt:
        some text
  steps:
    - Create file:
        details:
          file name: step1.txt
          content: some other text
```
engine.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty


class Engine(BaseEngine):
    given_definition = GivenDefinition(
        files_created=GivenProperty(),
    )

    def set_up(self):
        for filename, contents in self.given['files_created'].items():
            with open(filename, 'w') as handle:
                handle.write(contents)

    def create_file(self, details):
        with open(details['file name'], 'w') as handle:
            handle.write(details['content'])
```

With code:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine

```






```python
StoryCollection(Path(".").glob("*.story"), Engine()).named("Create files").play()

```

Will output:
```
RUNNING Create files in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
```




File preconditionfile.txt should now contain:

```
some text
```

File step1.txt should now contain:

```
some other text
```






!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/gradual-typing.story">gradual-typing.story
    storytests.</a>

