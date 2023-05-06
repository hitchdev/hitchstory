---
title: Story that rewrites the sub key of an argument
---



This shows how to build a story that rewrites a sub-key
of an argument.

```
self.current_step.rewrite("response", "content").to("new output")
```


# Code Example



example.story:

```yaml
REST API:
  steps:
  - API call:
      request:
        path: /hello
      response:
        status code: 200
        content: |
          {"old": "response"}
```
engine.py:

```python
from hitchstory import BaseEngine

class Engine(BaseEngine):
    def __init__(self, rewrite=True):
        self._rewrite = rewrite
    
    def run(self, command):
        pass

    def api_call(self, request, response):
        if self._rewrite:
            self.current_step.rewrite(
                "response", "content"
            ).to("""{"new": "output"}""")
```

With code:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine

```




## Story is rewritten when rewrite=True is used







```python
StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).ordered_by_name().play()

```

Will output:
```
RUNNING REST API in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
```




File example.story should now contain:

```
REST API:
  steps:
  - API call:
      request:
        path: /hello
      response:
        status code: 200
        content: |-
          {"new": "output"}
```


## Story remains unchanged when rewrite=False is used instead







```python
StoryCollection(Path(".").glob("*.story"), Engine(rewrite=False)).ordered_by_name().play()

```

Will output:
```
RUNNING REST API in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
```




Then the example story will be unchanged.







!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/rewrite-subkey-of-argument.story">rewrite-subkey-of-argument.story
    storytests.</a>

