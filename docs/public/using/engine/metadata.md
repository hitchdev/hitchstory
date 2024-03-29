---
title: Extra story metadata - e.g. adding JIRA ticket numbers to stories
---



Each and every story is related to issues on issue trackers,
specialist documentation, people, external resources and much more.

The best place to document this additional metadata is not buried in
word documents on company wikis but within the story itself.

What kind of metadata you add to stories is up to you -
simply add the names of the properties you want to add
in the info parameter of your engine InfoDefinition and
specify the structure of the metadata using StrictYAML
validators inside the InfoProperty object.

This example shows how you can add a series of JIRA tickets
and feature names as metadata on a story and filter stories
to play by JIRA ticket number.


# Code Example



example.story:

```yaml
Build city:
  about: Build a great city. The best.
  project jiras: JIRA-123, JIRA-124
  features: files, creating
  steps:
  - Reticulate splines

Live in city:
  project jiras: JIRA-789
  features: other
  steps:
  - Kick llama's ass

  variations:
    Build llama zoo:
      project jiras: JIRA-123
      features: zoo
      following steps:
      - Kick llama's ass
```

With code:

```python
from hitchstory import StoryCollection, BaseEngine, InfoDefinition, InfoProperty
from strictyaml import Map, Str, CommaSeparated, Optional
from pathlib import Path
from ensure import Ensure
from code_that_does_things import reticulate_splines, kick_llamas_ass

class Engine(BaseEngine):
    info_definition=InfoDefinition(
        project_jiras=InfoProperty(schema=CommaSeparated(Str())),
        features=InfoProperty(schema=CommaSeparated(Str())),
    )

    def reticulate_splines(self):
        print('reticulate splines')

    def kick_llamas_ass(self):
        print('kick llamas ass')

story_collection = StoryCollection(Path(".").glob("*.story"), Engine())

```




## Run all stories







```python
story_collection.ordered_by_name().play()
```

Will output:
```
RUNNING Build city in /path/to/working/example.story ... reticulate splines
SUCCESS in 0.1 seconds.
RUNNING Live in city in /path/to/working/example.story ... kick llamas ass
SUCCESS in 0.1 seconds.
RUNNING Live in city/Build llama zoo in /path/to/working/example.story ... kick llamas ass
kick llamas ass
SUCCESS in 0.1 seconds.
```





## Run only filtered stories







```python
story_collection.filter(lambda story: "JIRA-124" in story.info.get('project_jiras')).ordered_by_name().play()

```

Will output:
```
RUNNING Build city in /path/to/working/example.story ... reticulate splines
SUCCESS in 0.1 seconds.
```





## Info







```python
Ensure([story.info['project_jiras'] for story in story_collection.ordered_by_name()]).equals(
    [["JIRA-123", "JIRA-124"], ["JIRA-789", ], ["JIRA-123"]]
)

```









!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/metadata.story">metadata.story
    storytests.</a>

