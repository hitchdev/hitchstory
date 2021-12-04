---
title: Shortcut lookup for story names
---



Hunting for and specifying particular story to run can be a pain.

Using the 'shortcut' function you can select a specific story
to run just by specifying one or more key words that appear in
the story title. The case is ignored, as are special characters.

If you specify key words that match no stories or more than one
story, an error is raised.






example1.story:

```yaml
Create file:
  steps:
    - Create file
Create file again:
  steps:
    - Create file

```


example2.story:

```yaml
Create files:
  steps:
    - Create file

```








```python
from hitchstory import StoryCollection, BaseEngine
from ensure import Ensure
from pathquery import pathquery

class Engine(BaseEngine):
    def create_file(self, filename="step1.txt", content="example"):
        with open(filename, 'w') as handle:
            handle.write(content)

story_collection = StoryCollection(pathquery(".").ext("story"), Engine())

```




Story found and run:




```python
story_collection.shortcut("file", "again").play()

```

Will output:
```
RUNNING Create file again in /path/to/example1.story ... SUCCESS in 0.1 seconds.
```






Story not found:




```python
story_collection.shortcut("toast").play()
```


```python
hitchstory.exceptions.StoryNotFound:
Story 'toast' not found.
```






More than one story found:




```python
story_collection.shortcut("file").play()
```


```python
hitchstory.exceptions.MoreThanOneStory:
More than one matching story:
Create file (in /path/to/example1.story)
Create file again (in /path/to/example1.story)
Create files (in /path/to/example2.story)
```











!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/shortcut.story">shortcut.story
    storytests.</a>

