---
title: Creating a basic command line test runner
---



This example demonstrates the stories in the README
being run via a command line runner. It can be directly
copied and pasted.

If you prefer to run tests from within an existing testing
framework (e.g. pytest), see more on [how to do that here](../../pytest/dip-your-toe-hitchstory).

It uses the popular [click](https://click.palletsprojects.com/)
package to interpret command line arguments.


# Example



example.story:

```yaml
Log in as James:
  given:
    browser: firefox  # preconditions
  steps:
  - Enter text:
      username: james
      password: password
  - Click: log in
  
See James analytics:
  based on: log in as james  # inheritance
  following steps:
  - Click: analytics
```
test_hitchstory.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty
from hitchstory import Failure, strings_match
from hitchstory import StoryCollection
from strictyaml import Str
from pathlib import Path
from os import getenv

class Engine(BaseEngine):
    """Interprets and validates the hitchstory stories."""

    given_definition = GivenDefinition(
        browser=GivenProperty(Str()),
    )
    
    def __init__(self, rewrite=False):
        self._rewrite = rewrite

    def set_up(self):
        print(f"Using browser {self.given['browser']}")

    def click(self, name):
        print(f"Click on {name}")
        
        if name == "analytics":
            raise Failure(f"button {name} not found")
    
    def enter_text(self, **textboxes):
        for name, text in textboxes.items():
            print(f"Enter {text} in {name}")
    
    def tear_down(self):
        pass


collection = StoryCollection(
    # All *.story files in test_hitchstory.py's directory
    Path(__file__).parent.glob("*.story"),
    
    # If REWRITE environment variable is set to yes -> rewrite mode.
    Engine(rewrite=getenv("REWRITE", "no") == "yes")
)

#Create pytests that run stories manually:
#def test_log_in_as_james():
#    collection.named("Log in as james").play()

#def test_see_james_analytics():
#    collection.named("See James analytics").play()

# Dynamically stories as tests.
# E.g. "Log in as James" -> "def test_login_in_as_james"
collection.with_external_test_runner().ordered_by_name().add_pytests_to(
    module=__import__(__name__) # This module
)
```
runner.py:

```python
from hitchstory import StoryCollection
from click import argument, group, pass_context
from engine import Engine
from pathlib import Path

THIS_DIR = Path(__file__).absolute().parents[0]

STORIES = THIS_DIR.glob("*.story")

@group(invoke_without_command=True)
@pass_context
def cli(ctx):
    """Integration test command line interface."""
    pass

@cli.command()
@argument("keywords", nargs=-1)
def atdd(keywords):
    """
    Run single story with name matching keywords.
    """
    StoryCollection(STORIES, Engine())\
        .shortcut(*keywords)\
        .play()

@cli.command()
@argument("keywords", nargs=-1)
def ratdd(keywords):
    """
    Run single story with name matching keywords in rewrite mode.
    """
    StoryCollection(STORIES, Engine())\
        .shortcut(*keywords)\
        .play()

@cli.command()
def regression():
    """
    Run all tests.
    """
    StoryCollection(STORIES, Engine())\
        .only_uninherited()\
        .ordered_by_name()\
        .play()


if __name__ == "__main__":
    cli()
```




## Regular ATDD

Run a single test.







## Rewrite ATDD

Run a single test in rewrite mode.







## Regression

Run all tests.












!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/basic-cli.story">basic-cli.story
    storytests.</a>

