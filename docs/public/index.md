---
title: HitchStory
---

![](sliced-cucumber.jpg)

<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/hitchdev/hitchstory?style=social"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/hitchstory">

HitchStory is a python 
[testing and living documentation framework](approach/testing-and-living-documentation) for building strictly typed [executable specifications](approach/executable-specifications) which can [auto-generate your howto documentation](approach/triality).

The executable specifications can be written to specify, test and document applications at every level - replacing [xUnit](https://en.wikipedia.org/wiki/XUnit) equivalents of unit tests, integration tests and end to end tests with appropriate tooling.

The specifications are written using [StrictYAML](why/strictyaml).



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
from mockemailchecker import email_was_sent
from mockselenium import Webdriver
from strictyaml import Str

class Engine(BaseEngine):
    given_definition = GivenDefinition(
        website=GivenProperty(Str()),
    )

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

## Using HitchStory

- [Abort a story with ctrl-C](using/aborting)
- [Upgrade breaking changes between v0.14 and v0.15](using/breaking-changes-between-v014-and-v015)
- [Continue on failure when playing multiple stories](using/continue-on-failure)
- [Hiding stacktraces for expected exceptions](using/expected-exceptions)
- [Handling failing tests](using/failing-tests)
- [Flaky story detection](using/flaky-story-detection)
- [Generate documentation with extra variables and functions](using/generate-documentation)
- [Given preconditions](using/given)
- [Gradual typing of story steps](using/gradual-typing)
- [Story inheritance - given mapping preconditions overridden](using/inheritance-override-given-mapping)
- [Story inheritance - override given scalar preconditions](using/inheritance-override-given-scalar)
- [Story inheritance - parameters](using/inheritance-parameters)
- [Story inheritance - steps](using/inheritance-steps)
- [Inherit one story from another simply](using/inheritance)
- [Extra story metadata - e.g. adding JIRA ticket numbers to stories](using/metadata)
- [Story with parameters](using/parameterized-stories)
- [Play multiple stories in sequence](using/play-multiple-stories)
- [Story that rewrites itself](using/rewrite-story)
- [Running a single named story successfully](using/run-single-named-story)
- [Shortcut lookup for story names](using/shortcut-lookup)
- [Raising a Failure exception for known errors](using/special-failure-exception)
- [Arguments to steps](using/steps-and-step-arguments)
- [Strong typing](using/strong-typing)
- [Variations](using/variations)


## Approach to using HitchStory

Best practices, how the tool was meant to be used, etc.

- [Can I do BDD with hitchstory? How do I do BDD with hitchstory?](approach/bdd)
- [Complementary tools](approach/complementary-tools)
- [Executable specifications](approach/executable-specifications)
- [Flaky Tests](approach/flaky-tests)
- [Does hitchstory let your BA or Product Manager write stories while you just write the code?](approach/human-writable)
- [Recommended Environment](approach/recommended-environment)
- [Screenplay Principle](approach/screenplay-principle)
- [Separation of Test Concerns](approach/separation-of-test-concerns)
- [How can executable specifications and living documentation be used for stakeholder collaboration?](approach/stakeholder-collaboration)
- [Tests are an investment](approach/test-investment)
- [What is the difference betweeen a test and a story?](approach/test-or-story)
- [The importance of test realism](approach/test-realism)
- [What is a testing and living documentation framework?](approach/testing-and-living-documentation)
- [Testing non-deterministic code](approach/testing-nondeterministic-code)
- [Triality](approach/triality)


## Design decisions and principles

Design decisions are justified here:

- [Declarative User Stories](why/declarative)
- [Why does hitchstory mandate the use of given but not when and then?](why/given-when-then)
- [Why is inheritance a feature of hitchstory stories?](why/inheritance)
- [Why does hitchstory not have an opinion on what counts as interesting to "the business"?](why/interesting-to-the-business)
- [Why does hitchstory not have a command line interface?](why/no-cli)
- [Principles](why/principles)
- [Why programatically rewrite stories?](why/rewrite)
- [Why does HitchStory use StrictYAML?](why/strictyaml)


## Why not X instead?

There are several tools you can use instead, this is why you should use this one instead:

- [Why not use Behave, Lettuce or Cucumber (Gherkin)?](why-not/gherkin)
- [Why not use the Robot Framework?](why-not/robot)
- [Why use hitchstory instead of a unit testing framework?](why-not/unit-test)

