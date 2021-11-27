
---
title: Gradual typing of story steps
type: using
---



In order to speed up prototyping and development
of a story suite, the structure of your YAML data
specified in preconditions, parameters and step
arguments need not be specified in advance.

All data that is parsed without a validator
is parsed either as a dict, list or string, as
per the StrictYAML spec.

When your story suite matures and the structure of
your story files has solidified, you can
specify validators that fail fast when YAML
snippets with an invalid structure are used.




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



```python
from hitchstory import StoryCollection
from pathquery import pathquery
from engine import Engine

```






```python
StoryCollection(pathquery(".").ext("story"), Engine()).named("Create files").play()

```

Will output:
```
RUNNING Create files in /path/to/example.story ... SUCCESS in 0.1 seconds.
```






File preconditionfile.txt should now contain:

```
some text
```



File step1.txt should now contain:

```
some other text
```






{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/gradual-typing.story">gradual-typing.story</a>.
{{< /note >}}
