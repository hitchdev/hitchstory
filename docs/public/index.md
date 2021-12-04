---
title: HitchStory
---

![](sliced-cucumber.jpg)


<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/hitchdev/hitchstory?style=social"> 
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/hitchstory">



HitchStory is a python 3
[testing and living documentation framework](approach/testing-and-living-documentation) for building easily
maintained example driven [executable specifications](approach/executable-specifications) (sometimes dubbed
acceptance tests).

It was designed initially to make [realistic testing](approach/test-realism) of code less
of a chore so the tests would actually get written and run.

The executable specifications can be written to specify and test applications at
any level and have been used successfully to replace traditional
low level unit tests, integration tests and end to end tests
with easier to maintain tests.

The specifications are [written using StrictYAML](why/strictyaml) and the
code to execute them is written by you, in python.


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
  steps:
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
from hitchstory import StoryCollection
from pathquery import pathquery
from engine import Engine

StoryCollection(pathquery(".").ext("story"), Engine()).named("Email sent").play()

```

Will output:
```
RUNNING Email sent in /path/to/example.story ...
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












## Installation and set up

You *can* install hitchstory through pypi in any python 3 virtualenv:

```bash
$ pip install hitchstory
```

However, it's recommended to install and set up hitchstory with [hitchkey](https://github.com/hitchdev/hitchkey),
which will take care of automatically setting up a up the [recommended hitchstory environment](approach/recommended-environment).

Install hitchkey with [pipx](https://pypa.github.io/pipx/):

```bash
pipx install hitchkey
```

Once hitchkey is installed:

Example demo of hitchstory basics:

```bash
cd temp
hk --demo hitchstory ; hk bdd email
```

Example python API test demo (uses game of life):

```bash
cd temp
hk --demo pythonapi ; cd pythonapi ; hk bdd
```


## Using HitchStory

- [Abort a story with ctrl-C](using/alpha/aborting)
- [Continue on failure when playing multiple stories](using/alpha/continue-on-failure)
- [Hiding stacktraces for expected exceptions](using/alpha/expected-exceptions)
- [Handling failing tests](using/alpha/failing-tests)
- [Flaky story detection](using/alpha/flaky-story-detection)
- [Generate documentation from stories](using/alpha/generate-documentation)
- [Given preconditions](using/alpha/given)
- [Gradual typing of story steps](using/alpha/gradual-typing)
- [Inherit one story from another](using/alpha/inheritance)
- [Extra story metadata - e.g. adding JIRA ticket numbers to stories](using/alpha/metadata)
- [Story with parameters](using/alpha/parameterized-stories)
- [Play multiple stories in sequence](using/alpha/play-multiple-stories)
- [Story that rewrites itself](using/alpha/rewrite-story)
- [Running a single named story successfully](using/alpha/run-single-named-story)
- [Shortcut lookup for story names](using/alpha/shortcut-lookup)
- [Special exception named failure](using/alpha/special-failure-exception)
- [Arguments to steps](using/alpha/steps-and-step-arguments)
- [Strong typing](using/alpha/strong-typing)
- [Variations](using/alpha/variations)




## Approach to using HitchStory

Best practices, how the tool was meant to be used, etc.

- [Triality](approach/)
- [Testing non-deterministic code](approach/)
- [Executable specifications](approach/)
- [Recommended complementary tools](approach/)
- [Does hitchstory let your BA or Product Manager write stories while you just write the code?](approach/)
- [Screenplay Principle](approach/)
- [What is a testing and living documentation framework?](approach/)
- [Recommended Environment](approach/)
- [Can I do BDD with hitchstory? How do I do BDD with hitchstory?](approach/)
- [The importance of test realism](approach/)
- [What is the difference betweeen a test and a story?](approach/)
- [Flaky Tests](approach/)
- [Tests are an investment](approach/)
- [How can executable specifications and living documentation be used for stakeholder collaboration?](approach/)


## Design decisions and principles

Somewhat controversial design decisions are justified here.

- [Why does HitchStory use StrictYAML?](why/)
- [Why is inheritance a feature of hitchstory stories?](why/)
- [Why does hitchstory mandate the use of given but not when and then?](why/)
- [Two Unit Tests, Zero Integration Tests](why/)
- [Why does hitchstory not have a command line interface?](why/)
- [Why does hitchstory not have an opinion on what counts as interesting to "the business"?](why/)
- [Principles](why/)
- [Why programatically rewrite stories?](why/)
- [Declarative User Stories](why/)


## Why not X instead?

There are several tools you can use instead, this is why you should use this one instead:

- [Why not use the Robot Framework?](why-not/)
- [Why use hitchstory instead of a unit testing framework?](why-not/)
- [Why not use Behave, Lettuce or Cucumber (Gherkin)?](why-not/)
