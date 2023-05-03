---
title: HitchStory
---

![](sliced-cucumber.jpg)

<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/hitchdev/hitchstory?style=social"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/hitchstory">

HitchStory is a [StrictYAML](why/strictyaml) based python integration testing framework where the tests can [rewrite themselves](why/rewrite) and [write your docs](approach/triality).

[![Test rewriting itself](https://hitchdev.com/images/video-thumb.png)](https://vimeo.com/822561823 "Test rewriting itself")

It can be used to quickly and easily integration test and generate docs for any kind of app. Examples:

* [A website](https://github.com/hitchdev/hitchstory/tree/master/examples/website)
* [An interactive command line app](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline)
* [A REST API](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi)
* [A Python API](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi)


## Example





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






```python
>>> from hitchstory import StoryCollection
>>> from pathlib import Path
>>> from engine import Engine
>>> 
>>> StoryCollection(Path(".").glob("*.story"), Engine()).named("Email sent").play()
RUNNING Email sent in /path/to/working/example.story ... Load web page at /login
Put hunter2 in name
Put AzureDiamond in name
Click on login
Click on new email
Put Hey guys,

I think I got hacked!
 in name
Put Cthon98@aol.com in name
Click on send email
Check email was sent!
SUCCESS in 0.1 seconds.
```








## Install

```bash
$ pip install hitchstory
```

## Using HitchStory: Setup

Skeleton set up with example stories:

- [Creating a basic command line test runner](using/setup/basic-cli)


## Using HitchStory: With Pytest

If you already have pytest set up and running integration
tests, you can use it with hitchstory:

- [Dip your toe in the water with pytest](using/pytest/dip-your-toe-hitchstory)
- [Self rewriting tests with pytest and hitchstory](using/pytest/rewrite)


## Using HitchStory: Engine

How to use the different features of the story engine:

- [Hiding stacktraces for expected exceptions](using/engine/expected-exceptions)
- [Given preconditions](using/engine/given)
- [Gradual typing of story steps](using/engine/gradual-typing)
- [Match two JSON snippets](using/engine/match-json)
- [Match two strings and show diff on failure](using/engine/match-two-strings)
- [Extra story metadata - e.g. adding JIRA ticket numbers to stories](using/engine/metadata)
- [Story with parameters](using/engine/parameterized-stories)
- [Story that rewrites itself](using/engine/rewrite-story)
- [Raising a Failure exception to conceal the stacktrace](using/engine/special-failure-exception)
- [Arguments to steps](using/engine/steps-and-step-arguments)
- [Strong typing](using/engine/strong-typing)


## Using HitchStory: Documentation Generation

How to autogenerate documentation from your tests:

- [Generate documentation with extra variables and functions](using/documentation/extra)
- [Generate documentation from story](using/documentation/generate)


## Using HitchStory: Inheritance

Inheriting stories from each other:

- [Inherit one story from another simply](using/inheritance/about)
- [Story inheritance - given mapping preconditions overridden](using/inheritance/override-given-mapping)
- [Story inheritance - override given scalar preconditions](using/inheritance/override-given-scalar)
- [Story inheritance - parameters](using/inheritance/parameters)
- [Story inheritance - steps](using/inheritance/steps)
- [Variations](using/inheritance/variations)


## Using HitchStory: Runner

Running the stories in different ways:

- [Continue on failure when playing multiple stories](using/runner/continue-on-failure)
- [Flaky story detection](using/runner/flaky-story-detection)
- [Play multiple stories in sequence](using/runner/play-multiple-stories-in-sequence)
- [Run one story in collection](using/runner/run-just-one-story)
- [Shortcut lookup for story names](using/runner/shortcut-lookup)


## Approach to using HitchStory

Best practices, how the tool was meant to be used, etc.

- [Can I do BDD with hitchstory? How do I do BDD with hitchstory?](approach/bdd)
- [Complementary tools](approach/complementary-tools)
- [Executable specifications](approach/executable-specifications)
- [Flaky Tests](approach/flaky-tests)
- [Does hitchstory let "the business" write stories while you just write the code?](approach/human-writable)
- [Separation of Test Concerns](approach/separation-of-test-concerns)
- [Test Artefact Environment Isolation](approach/test-artefact-environment-isolation)
- [Test concern leakage](approach/test-concern-leakage)
- [Tests as an investment](approach/test-investment)
- [What is the difference betweeen a test and a story?](approach/test-or-story)
- [The importance of test realism](approach/test-realism)
- [Testing non-deterministic code](approach/testing-nondeterministic-code)
- [Specification Documentation Test Triality](approach/triality)


## Design decisions and principles

Design decisions are justified here:

- [Declarative User Stories](why/declarative)
- [Why does hitchstory mandate the use of given but not when and then?](why/given-when-then)
- [Why is inheritance a feature of hitchstory stories?](why/inheritance)
- [Why does hitchstory not have an opinion on what counts as interesting to "the business"?](why/interesting-to-the-business)
- [Why does hitchstory not have a command line interface?](why/no-cli)
- [Principles](why/principles)
- [Why does HitchStory have no CLI runner - only a pure python API?](why/pure-python-no-cli)
- [Why Rewritable Test Driven Development (RTDD)?](why/rewrite)
- [Why does HitchStory use StrictYAML?](why/strictyaml)


## Why not X instead?

HitchStory is not the only integration testing framework.
This is how it compares with the others:

- [Why use Hitchstory instead of Behave, Lettuce or Cucumber (Gherkin)?](why-not/gherkin)
- [Why not use the Robot Framework?](why-not/robot)
- [Why use hitchstory instead of a unit testing framework?](why-not/unit-test)


## Using HitchStory: Behavior

Miscellaneous docs about behavior of the framework:

- [Abort a story with ctrl-C](using/behavior/aborting)
- [Upgrade breaking changes between v0.14 and v0.15](using/behavior/breaking-changes-between-v014-and-v015)
- [Handling failing tests](using/behavior/failing-tests)
- [Running a single named story successfully](using/behavior/run-single-named-story)

