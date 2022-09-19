---
title: Story that rewrites itself
---



Hitch stories can be partially rewritten when the code
is changed when a step involves verifying a block of text.

It is a time saver when you only want to make modifications to
messages output by a program and ensure that those modifications
are verified.

Instead of manually constructing the exact output you are expecting
you can simply visually inspect the output to verify that it is
the desired output.

This example shows a story being run in "rewrite" mode - where
text strings are rewritten. This mode can be used when doing development
when you expect textual changes.

If the story passes then the file will be rewritten with the updated
contents. If the story fails for any reason then the file will not
be touched.

If rewrite=False is fed through to the story engine instead, the story
will always fail when seeing different text. This mode can be used when,
for example, running all the stories on jenkins or when you are refactoring
and *not* expecting textual output changes.




example.story:

```yaml
Do things:
  steps:
    - Do thing: x
    - Do thing: y
    - Do thing: z
    - Do other thing:
        variable 1: a
        variable_2: b

  variations:
    Do more things:
      steps:
        - Do thing: c

```









engine.py:

```python
from hitchstory import BaseEngine

class Engine(BaseEngine):
    def __init__(self, rewrite=True):
        self._rewrite = rewrite

    def do_thing(self, variable):
        if self._rewrite:
            self.current_step.update(
                variable="xxx:\nyyy"
            )

    def do_other_thing(self, variable_1=None, variable_2=None):
        if self._rewrite:
            self.current_step.update(
                variable_2="complicated:\nmultiline\nstring"
            )

```



```python
from hitchstory import StoryCollection
from pathquery import pathquery
from engine import Engine

```




Rewritten:




```python
StoryCollection(pathquery(".").ext("story"), Engine(rewrite=True)).ordered_by_name().play()

```

Will output:
```
RUNNING Do things in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
RUNNING Do things/Do more things in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
```








No changes:




```python
StoryCollection(pathquery(".").ext("story"), Engine(rewrite=False)).ordered_by_name().play()

```

Will output:
```
RUNNING Do things in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
RUNNING Do things/Do more things in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
```






Then the example story will be unchanged.








!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/rewrite-story.story">rewrite-story.story
    storytests.</a>

