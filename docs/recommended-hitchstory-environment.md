---
title: Recommended HitchStory Environment
---

HitchStory was designed and built on the presumption that it would always be run in a *different* environment
to the environment used to run the code. This is in stark contrast to how unit testing frameworks are presumed
to run - i.e. in python, in the same virtualenv.

There are two reasons for this:

* HitchStory dependencies and related tools are unable to conflict with application code if they run in a separate, segrated environment.

* If segregated, HitchStory and its related tools can be used to *set up* testing and development environments.


HitchStory was also designed to only be run *indirectly from* the command line, like this example which is pulled 
directly from this project's key.py file:

```python
@expected(exceptions.HitchStoryException)
def bdd(*keywords):
    """
    Run story with name containing keywords.
    """
    _storybook({
        "overwrite artefacts": False, "print output": True,
    }).shortcut(*keywords).play()
```

This is done because while a lot of the time the configuration of how tests are run is simple - requiring
just a one liner, far too frequently it becomes necessary to change the behavior of how tests are run - often
in a complex way.
