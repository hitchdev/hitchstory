---
title: Creating a basic command line test runner
---



This example demonstrates the stories in the README
being run via a command line runner. It can be directly
copied and pasted.

If you prefer to run tests from within an existing testing
framework (e.g. pytest), see more on [how to do that here](../pytest).

It uses the popular [click](https://click.palletsprojects.com/)
package to interpret command line arguments.


# Example



example.story:

```yaml
Logged in:
  given:
    website: /login  # preconditions
  steps:
  - Form filled:
      username: AzureDiamond
      password: hunter2
  - Clicked: login


Email sent:
  about: |
    The most basic email with no subject, cc or bcc
    set.
  based on: logged in             # inherits from and continues from test above
  following steps:
  - Clicked: new email
  - Form filled:
      to: Cthon98@aol.com
      contents: |                # long form text
        Hey guys,

        I think I got hacked!
  - Clicked: send email
  - Email was sent
```
engine.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty
from hitchstory import Failure, strings_match
from strictyaml import Str

class Engine(BaseEngine):
    given_definition = GivenDefinition(
        website=GivenProperty(Str()),
    )
    
    def __init__(self, rewrite=False):
        self._rewrite = rewrite

    def set_up(self):
        print(f"Load web page at {self.given['website']}")

    def form_filled(self, **textboxes):
        for name, contents in sorted(textboxes.items()):
            print(f"Put {contents} in name")

    def clicked(self, name):
        print(f"Click on {name}")
    
    def failing_step(self):
        raise Failure("This was not supposed to happen")
    
    def error_message_displayed(self, expected_message):
        """Demonstrates steps that can rewrite themselves."""
        actual_message = "error message!"
        try:
            strings_match(expected_message, actual_message)
        except Failure:
            if self._rewrite:
                self.current_step.rewrite("expected_message").to(actual_message)
            else:
                raise

    def email_was_sent(self):
        print("Check email was sent!")
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

