# HitchStory

[![Main branch status](https://github.com/hitchdev/hitchstory/actions/workflows/regression.yml/badge.svg)](https://github.com/hitchdev/hitchstory/actions/workflows/regression.yml)

HitchStory is a [StrictYAML](https://hitchdev.com/hitchstory/why/strictyaml) based python integration testing framework where the tests can [rewrite themselves](https://hitchdev.com/hitchstory/why/rewrite) and [write your docs](https://hitchdev.com/hitchstory/approach/triality).

[![Test rewriting itself](https://hitchdev.com/images/video-thumb.png)](https://vimeo.com/822561823 "Test rewriting itself")

It can be used to quickly and easily integration test and generate docs for any kind of app. Examples:

* [A website](https://github.com/hitchdev/hitchstory/tree/master/examples/website)
* [An interactive command line app](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline)
* [A REST API](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi)
* [A Python API](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi)


## Example







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
from mockemailchecker import email_was_sent
from mockselenium import Webdriver
from strictyaml import Str

class Engine(BaseEngine):
    given_definition = GivenDefinition(
        website=GivenProperty(Str()),
    )
    
    def __init__(self, rewrite=False):
        self._rewrite = rewrite

    def set_up(self):
        self.driver = Webdriver()
        self.driver.visit(
            "http://localhost:5000{0}".format(self.given['website'])
        )

    def form_filled(self, **textboxes):
        for name, contents in sorted(textboxes.items()):
            self.driver.fill_form(name, contents)

    def clicked(self, name):
        self.driver.click(name)
    
    def failing_step(self):
        raise Failure("This was not supposed to happen")
    
    def error_message_displayed(self, expected_message):
        """Demonstrates steps that can rewrite themselves."""
        actual_message = "error message!"
        try:
            strings_match(expected_message, actual_message)
        except Failure:
            self.current_step.rewrite("expected_message").to(actual_message)

    def email_was_sent(self):
        email_was_sent()
```






```python
>>> from hitchstory import StoryCollection
>>> from pathlib import Path
>>> from engine import Engine
>>> 
>>> StoryCollection(Path(".").glob("*.story"), Engine()).named("Email sent").play()
RUNNING Email sent in /path/to/working/example.story ...
Visiting http://localhost:5000/login
Entering text hunter2 in password
Entering text AzureDiamond in username
Clicking on login
Clicking on new email
In contents entering text:
Hey guys,

I think I got hacked!


Entering text Cthon98@aol.com in to
Clicking on send email
Email was sent
SUCCESS in 0.1 seconds.
```








## Install

```bash
$ pip install hitchstory
```

## Using HitchStory: Setup

- [Creating a basic command line test runner](https://hitchdev.com/hitchstory/using/setup/basic-cli)
- [Using hitchstory with pytest](https://hitchdev.com/hitchstory/using/setup/pytest)


## Using HitchStory: Engine

- [Hiding stacktraces for expected exceptions](https://hitchdev.com/hitchstory/using/engine/expected-exceptions)
- [Given preconditions](https://hitchdev.com/hitchstory/using/engine/given)
- [Gradual typing of story steps](https://hitchdev.com/hitchstory/using/engine/gradual-typing)
- [Match two strings and show diff on failure](https://hitchdev.com/hitchstory/using/engine/match-two-strings)
- [Extra story metadata - e.g. adding JIRA ticket numbers to stories](https://hitchdev.com/hitchstory/using/engine/metadata)
- [Story that rewrites itself](https://hitchdev.com/hitchstory/using/engine/rewrite-story)
- [Raising a Failure exception to conceal the stacktrace](https://hitchdev.com/hitchstory/using/engine/special-failure-exception)
- [Arguments to steps](https://hitchdev.com/hitchstory/using/engine/steps-and-step-arguments)
- [Strong typing](https://hitchdev.com/hitchstory/using/engine/strong-typing)


## Using HitchStory

- [Abort a story with ctrl-C](https://hitchdev.com/hitchstory/using/aborting)
- [Upgrade breaking changes between v0.14 and v0.15](https://hitchdev.com/hitchstory/using/breaking-changes-between-v014-and-v015)
- [Continue on failure when playing multiple stories](https://hitchdev.com/hitchstory/using/continue-on-failure)
- [Handling failing tests](https://hitchdev.com/hitchstory/using/failing-tests)
- [Flaky story detection](https://hitchdev.com/hitchstory/using/flaky-story-detection)
- [Generate documentation with extra variables and functions](https://hitchdev.com/hitchstory/using/generate-documentation)
- [Story inheritance - given mapping preconditions overridden](https://hitchdev.com/hitchstory/using/inheritance-override-given-mapping)
- [Story inheritance - override given scalar preconditions](https://hitchdev.com/hitchstory/using/inheritance-override-given-scalar)
- [Story inheritance - parameters](https://hitchdev.com/hitchstory/using/inheritance-parameters)
- [Story inheritance - steps](https://hitchdev.com/hitchstory/using/inheritance-steps)
- [Inherit one story from another simply](https://hitchdev.com/hitchstory/using/inheritance)
- [Story with parameters](https://hitchdev.com/hitchstory/using/parameterized-stories)
- [Play multiple stories in sequence](https://hitchdev.com/hitchstory/using/play-multiple-stories)
- [Running a single named story successfully](https://hitchdev.com/hitchstory/using/run-single-named-story)
- [Shortcut lookup for story names](https://hitchdev.com/hitchstory/using/shortcut-lookup)
- [Variations](https://hitchdev.com/hitchstory/using/variations)


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

There are several tools you can use instead, this is why you should use this one instead:

- [Why use Hitchstory instead of Behave, Lettuce or Cucumber (Gherkin)?](https://hitchdev.com/hitchstory/why-not/gherkin)
- [Why not use the Robot Framework?](https://hitchdev.com/hitchstory/why-not/robot)
- [Why use hitchstory instead of a unit testing framework?](https://hitchdev.com/hitchstory/why-not/unit-test)

