# HitchStory

[![Main branch status](https://github.com/hitchdev/hitchstory/actions/workflows/regression.yml/badge.svg)](https://github.com/hitchdev/hitchstory/actions/workflows/regression.yml)

Type-safe [StrictYAML](https://hitchdev.com/hitchstory/why/strictyaml) integration tests run from pytest. They can:

## Rewrite themselves from program output (command line test example)

![Test rewriting itself](https://hitchdev-videos.netlify.app/rewrite-demo.gif)

## Autogenerate documentation (website test example)

![Test writing docs](https://hitchdev-videos.netlify.app/rewrite-docs-demo.gif)


## Demo projects with demo tests

Project | Storytests | Python code | Doc template | Autogenerated docs
---|---|---|---|---
[Website](https://github.com/hitchdev/hitchstory/tree/master/examples/website) | [add todo](https://github.com/hitchdev/hitchstory/tree/master/examples/website/story/add-todo.story), [correct spelling](https://github.com/hitchdev/hitchstory/tree/master/examples/website/story/correct-my-spelling.story) | [test_integration.py](https://github.com/hitchdev/hitchstory/tree/master/examples/website/tests/test_integration.py) | [docstory.yml](https://github.com/hitchdev/hitchstory/tree/master/examples/website/tests/docstory.yml) | [Add todo](https://github.com/hitchdev/hitchstory/blob/master/examples/website/docs/add-and-retrieve-todo.md), [Correct my spelling](https://github.com/hitchdev/hitchstory/tree/master/examples/website/docs/correct-my-spelling.md)
[REST API](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi) | [add todo](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi/story/add-todo.story), [correct spelling](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi/story/correct-my-spelling.story) | [test_integration.py](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi/tests/test_integration.py) | [docstory.yml](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi/tests/docstory.yml) | [Add todo](https://github.com/hitchdev/hitchstory/blob/master/examples/restapi/docs/add-and-retrieve-todo.md), [Correct my spelling](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi/docs/correct-my-spelling.md)
[Interactive command line app](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline) | [add todo](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline/story/add-todo.story), [correct spelling](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline/story/correct-my-spelling.story) | [test_integration.py](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline/tests/test_integration.py) | [docstory.yml](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline/tests/docstory.yml) | [Add todo](https://github.com/hitchdev/hitchstory/blob/master/examples/commandline/docs/add-and-retrieve-todo.md), [Correct my spelling](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline/docs/correct-my-spelling.md)
[A Python API](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi) | [add todo](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi/story/add-todo.story), [correct spelling](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi/story/correct-my-spelling.story) | [engine.py](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi/tests/engine.py) | [docstory.yml](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi/tests/docstory.yml) | [Add todo](https://github.com/hitchdev/hitchstory/blob/master/examples/pythonapi/docs/add-and-retrieve-todo.md), [Correct my spelling](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi/docs/correct-my-spelling.md)




Minimal example (two files) demonstrating two short YAML tests and the 
python code necessary to run them from within a pytest file.


# Code Example



example.story:

```yaml
Log in as James:
  given:
    browser: firefox  # test preconditions
  steps:
  - Enter text:
      username: james
      password: password
  - Click: log in
  
See James analytics:
  based on: log in as james  # test inheritance
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
        browser=GivenProperty(
            # Available validators: https://hitchdev.com/strictyaml/using/
            Str()
        ),
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
    # All .story files in this file's directory.
    Path(__file__).parent.glob("*.story"),

    Engine(
        # If REWRITE environment variable is set to yes -> rewrite mode.
        rewrite=getenv("REWRITE", "no") == "yes"
    )
)

#You can embed the stories in tests manually:
#def test_log_in_as_james():
#    collection.named("Log in as james").play()

#def test_see_james_analytics():
#    collection.named("See James analytics").play()

# Or autogenerate runnable tests from the YAML stories like so:
# E.g. "Log in as James" -> "def test_login_in_as_james"
collection.with_external_test_runner().ordered_by_name().add_pytests_to(
    module=__import__(__name__) # This module
)
```




## Run passing "log in as James" test

Running test_log_in_as_james runs the "Log in as James" story.





`pytest -s -k test_log_in_as_james`

Outputs:
```
============================= test session starts ==============================
platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
rootdir: /path/to
collected 2 items / 1 deselected / 1 selected

test_hitchstory.py Using browser firefox
Enter james in username
Enter password in password
Click on log in
.

======================= 1 passed, 1 deselected in 0.1s ========================
```


## Run failing "see James' analytics" test

Failing tests also have colors and highlighting when run for real.





`pytest -k test_see_james_analytics`

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
E       hitchstory.exceptions.StoryFailure: RUNNING See James analytics in /path/to/example.story ... FAILED in 0.1 seconds.
E
E             based on: log in as james  # test inheritance
E             following steps:
E             - Click: analytics
E
E
E       hitchstory.exceptions.Failure
E
E           Test failed.
E
E       button analytics not found

/src/hitchstory/story_list.py:51: StoryFailure
----------------------------- Captured stdout call -----------------------------
Using browser firefox
Enter james in username
Enter password in password
Click on log in
Click on analytics
=========================== short test summary info ============================
FAILED test_hitchstory.py::test_see_james_analytics - hitchstory.exceptions.StoryFailure: RUNNING See James analytics in /path/to/example.story ... FAILED in 0.1 seconds.

      based on: log in as james  # test inheritance
      following steps:
      - Click: analytics


hitchstory.exceptions.Failure

    Test failed.

button analytics not found
======================= 1 failed, 1 deselected in 0.1s ========================
```








## Install

```bash
$ pip install hitchstory
```

## Using HitchStory

Every feature of this library is documented and listed below.
It is tested and documented with itself.


## Using HitchStory: With Pytest

If you already have pytest set up and running integration
tests, you can use it with hitchstory:

- [Self rewriting tests with pytest and hitchstory](https://hitchdev.com/hitchstory/using/pytest/rewrite)


## Using HitchStory: Engine

How to use the different features of the story engine:

- [Hiding stacktraces for expected exceptions](https://hitchdev.com/hitchstory/using/engine/expected-exceptions)
- [Given preconditions](https://hitchdev.com/hitchstory/using/engine/given)
- [Gradual typing of story steps](https://hitchdev.com/hitchstory/using/engine/gradual-typing)
- [Match two JSON snippets](https://hitchdev.com/hitchstory/using/engine/match-json)
- [Match two strings and show diff on failure](https://hitchdev.com/hitchstory/using/engine/match-two-strings)
- [Extra story metadata - e.g. adding JIRA ticket numbers to stories](https://hitchdev.com/hitchstory/using/engine/metadata)
- [Story with parameters](https://hitchdev.com/hitchstory/using/engine/parameterized-stories)
- [Story that rewrites itself](https://hitchdev.com/hitchstory/using/engine/rewrite-story)
- [Story that rewrites the sub key of an argument](https://hitchdev.com/hitchstory/using/engine/rewrite-subkey-of-argument)
- [Raising a Failure exception to conceal the stacktrace](https://hitchdev.com/hitchstory/using/engine/special-failure-exception)
- [Arguments to steps](https://hitchdev.com/hitchstory/using/engine/steps-and-step-arguments)
- [Strong typing](https://hitchdev.com/hitchstory/using/engine/strong-typing)


## Using HitchStory: Documentation Generation

How to autogenerate documentation from your tests:

- [Generate documentation with extra variables and functions](https://hitchdev.com/hitchstory/using/documentation/extra)
- [Generate documentation from story](https://hitchdev.com/hitchstory/using/documentation/generate)


## Using HitchStory: Inheritance

Inheriting stories from each other:

- [Inherit one story from another simply](https://hitchdev.com/hitchstory/using/inheritance/about)
- [Story inheritance - given mapping preconditions overridden](https://hitchdev.com/hitchstory/using/inheritance/override-given-mapping)
- [Story inheritance - override given scalar preconditions](https://hitchdev.com/hitchstory/using/inheritance/override-given-scalar)
- [Story inheritance - parameters](https://hitchdev.com/hitchstory/using/inheritance/parameters)
- [Story inheritance - steps](https://hitchdev.com/hitchstory/using/inheritance/steps)
- [Variations](https://hitchdev.com/hitchstory/using/inheritance/variations)


## Using HitchStory: Runner

Running the stories in different ways:

- [Continue on failure when playing multiple stories](https://hitchdev.com/hitchstory/using/runner/continue-on-failure)
- [Flaky story detection](https://hitchdev.com/hitchstory/using/runner/flaky-story-detection)
- [Play multiple stories in sequence](https://hitchdev.com/hitchstory/using/runner/play-multiple-stories-in-sequence)
- [Run one story in collection](https://hitchdev.com/hitchstory/using/runner/run-just-one-story)
- [Shortcut lookup for story names](https://hitchdev.com/hitchstory/using/runner/shortcut-lookup)


## Approach to using HitchStory

Best practices, how the tool was meant to be used, etc.

- [Can I do BDD with hitchstory? How do I do BDD with hitchstory?](https://hitchdev.com/hitchstory/approach/bdd)
- [Complementary tools](https://hitchdev.com/hitchstory/approach/complementary-tools)
- [Executable specifications](https://hitchdev.com/hitchstory/approach/executable-specifications)
- [Flaky Tests](https://hitchdev.com/hitchstory/approach/flaky-tests)
- [Does hitchstory let "the business" write stories while you just write the code?](https://hitchdev.com/hitchstory/approach/human-writable)
- [Separation of Test Concerns](https://hitchdev.com/hitchstory/approach/separation-of-test-concerns)
- [Test Artefact Environment Isolation](https://hitchdev.com/hitchstory/approach/test-artefact-environment-isolation)
- [Test concern leakage](https://hitchdev.com/hitchstory/approach/test-concern-leakage)
- [Tests as an investment](https://hitchdev.com/hitchstory/approach/test-investment)
- [What is the difference betweeen a test and a story?](https://hitchdev.com/hitchstory/approach/test-or-story)
- [The importance of test realism](https://hitchdev.com/hitchstory/approach/test-realism)
- [Testing non-deterministic code](https://hitchdev.com/hitchstory/approach/testing-nondeterministic-code)
- [Specification Documentation Test Triality](https://hitchdev.com/hitchstory/approach/triality)


## Design decisions and principles

Design decisions are justified here:

- [Declarative User Stories](https://hitchdev.com/hitchstory/why/declarative)
- [Why does hitchstory mandate the use of given but not when and then?](https://hitchdev.com/hitchstory/why/given-when-then)
- [Why is inheritance a feature of hitchstory stories?](https://hitchdev.com/hitchstory/why/inheritance)
- [Why does hitchstory not have an opinion on what counts as interesting to "the business"?](https://hitchdev.com/hitchstory/why/interesting-to-the-business)
- [Why does hitchstory not have a command line interface?](https://hitchdev.com/hitchstory/why/no-cli)
- [Principles](https://hitchdev.com/hitchstory/why/principles)
- [Why does HitchStory have no CLI runner - only a pure python API?](https://hitchdev.com/hitchstory/why/pure-python-no-cli)
- [Why Rewritable Test Driven Development (RTDD)?](https://hitchdev.com/hitchstory/why/rewrite)
- [Why does HitchStory use StrictYAML?](https://hitchdev.com/hitchstory/why/strictyaml)


## Why not X instead?

HitchStory is not the only integration testing framework.
This is how it compares with the others:

- [Why use Hitchstory instead of Behave, Lettuce or Cucumber (Gherkin)?](https://hitchdev.com/hitchstory/why-not/gherkin)
- [Why not use the Robot Framework?](https://hitchdev.com/hitchstory/why-not/robot)
- [Why use hitchstory instead of a unit testing framework?](https://hitchdev.com/hitchstory/why-not/unit-test)


## Using HitchStory: Setup on its own

If you want to use HitchStory without pytest:

- [Creating a basic command line test runner](https://hitchdev.com/hitchstory/using/setup/basic-cli)


## Using HitchStory: Behavior

Miscellaneous docs about behavior of the framework:

- [Abort a story with ctrl-C](https://hitchdev.com/hitchstory/using/behavior/aborting)
- [Upgrade breaking changes between v0.14 and v0.15](https://hitchdev.com/hitchstory/using/behavior/breaking-changes-between-v014-and-v015)
- [Handling failing tests](https://hitchdev.com/hitchstory/using/behavior/failing-tests)
- [Running a single named story successfully](https://hitchdev.com/hitchstory/using/behavior/run-single-named-story)

