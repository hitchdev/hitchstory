---
title: Running a single named story successfully
---



How a story runs when it is successful - i.e. when no exception
is raised during its run.


# Example



example.story:

```yaml
Create files:
  steps:
    - Create file
    - Create file: step2.txt
    - Create file:
        file name: step3.txt
        content: third step
```
engine.py:

```python
from hitchstory import BaseEngine


class Engine(BaseEngine):
    def create_file(self, file_name="step1.txt", content="example"):
        with open(file_name, 'w') as handle:
            handle.write(content)

    def on_success(self):
        print("splines reticulated")

        with open("ranstory.txt", 'w') as handle:
            handle.write(self.story.name)
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
RUNNING Create files in /path/to/working/example.story ... splines reticulated
SUCCESS in 0.1 seconds.
```




File step1.txt should now contain:

```
example
```

File step2.txt should now contain:

```
example
```

File step3.txt should now contain:

```
third step
```

File ranstory.txt should now contain:

```
Create files
```






!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/success.story">success.story
    storytests.</a>

