---
title: HitchStory
---

![](sliced-cucumber.jpg)

<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/hitchdev/hitchstory?style=social"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/hitchstory">

HitchStory is a [StrictYAML](why/strictyaml) based python integration testing library
that runs in pytest.

With it, you can write [integration tests that rewrite themselves](why/rewrite) and [tests that write your docs](approach/triality):

[![Test rewriting itself](https://hitchdev.com/images/video-thumb.png)](https://vimeo.com/822561823 "Test rewriting itself")

It can be used to quickly and easily integration test and generate docs for any kind of app. Examples:

* [A website](https://github.com/hitchdev/hitchstory/tree/master/examples/website)
* [An interactive command line app](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline)
* [A REST API](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi)
* [A Python API](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi)




If you would like to dip your toe into the water
with hitchstory integration tests, you can `pip install hitchstory`
and copy and paste the following two files below into a test folder:


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




## The log in test passes






Running: `pytest -k test_log_in_as_james test_hitchstory.py`

Outputs:
```
============================= test session starts ==============================
platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
rootdir: /path/to
collected 2 items / 1 deselected / 1 selected

test_hitchstory.py .                                                     [100%]

======================= 1 passed, 1 deselected in 0.1s ========================
```


## See James' analytics test fails






Running: `pytest -k test_see_james_analytics test_hitchstory.py`

Outputs:
```
============================= test session starts ==============================
platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
rootdir: /path/to
collected 2 items / 1 deselected / 1 selected

test_hitchstory.py F                                                     [100%]

=================================== FAILURES ===================================
___________________________ test_see_james_analytics ___________________________

story = Story('see-james-analytics')

    def hitchstory(story=story):
>       story.play()
E       hitchstory.exceptions.StoryFailure: RUNNING See James analytics in /path/to/example.story ... [[ RED ]][[ BRIGHT ]]FAILED in 0.1 seconds.[[ RESET ALL ]]
E
E       [[ BLUE ]]      based on: log in as james  # inheritance
E             following steps:
E           [[ BRIGHT ]]  - Click: analytics[[ NORMAL ]]
E           [[ RESET ALL ]]
E
E       [[ RED ]][[ BRIGHT ]]hitchstory.exceptions.Failure[[ RESET ALL ]]
E         [[ DIM ]][[ RED ]]
E           Test failed.
E           [[ RESET ALL ]]
E       [[ RED ]]button analytics not found[[ RESET FORE ]]

/src/hitchstory/story_list.py:50: StoryFailure
----------------------------- Captured stdout call -----------------------------
Using browser firefox
Enter james in username
Enter password in password
Click on log in
Click on analytics
=========================== short test summary info ============================
FAILED test_hitchstory.py::test_see_james_analytics - hitchstory.exceptions.StoryFailure: RUNNING See James analytics in /path/to/example.story ... [[ RED ]][[ BRIGHT ]]FAILED in 0.1 seconds.[[ RESET ALL ]]

[[ BLUE ]]      based on: log in as james  # inheritance
      following steps:
    [[ BRIGHT ]]  - Click: analytics[[ NORMAL ]]
    [[ RESET ALL ]]

[[ RED ]][[ BRIGHT ]]hitchstory.exceptions.Failure[[ RESET ALL ]]
  [[ DIM ]][[ RED ]]
    Test failed.
    [[ RESET ALL ]]
[[ RED ]]button analytics not found[[ RESET FORE ]]
======================= 1 failed, 1 deselected in 0.1s ========================
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

