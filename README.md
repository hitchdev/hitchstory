# HitchStory


HitchStory is a python 3
[testing and living documentation framework](https://hitchdev.com/hitchstory/approach/testing-and-living-documentation) for building easily
maintained example driven [executable specifications](https://hitchdev.com/hitchstory/approach/executable-specifications) (sometimes dubbed
acceptance tests).

It was designed initially to make [realistic testing](https://hitchdev.com/hitchstory/approach/test-realism) of code less
of a goddamn chore so the tests would actually get written and run.

The executable specifications can be written to specify and test applications at
any level and have been used successfully to replace traditional
[low level unit tests](https://hitchdev.com/hitchstory/), [integration tests](https://hitchdev.com/hitchstory/) and [end to end tests](https://hitchdev.com/hitchstory/)
with easier to maintain tests.

The specifications are [written using StrictYAML](https://hitchdev.com/hitchstory/why/strictyaml) and the
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
which will take care of automatically setting up a up the [recommended hitchstory environment](https://hitchdev.com/hitchstory/approach/recommended-environment).

Either install hitchkey with [pipsi](https://github.com/mitsuhiko/pipsi):

```bash
pipsi install hitchkey
```

Or, if you'd prefer, you can safely install with "sudo pip":

```bash
sudo pip install hitchkey
```

Once hitchkey is installed:

```bash
cd /your/project/directory
hk --tutorial hitchstory
```

This will create a directory called "hitch" and put three files in it, including one story, which you can play by running:

```bash
hk bdd my first
```


## Using HitchStory

- [Arguments to steps](https://hitchdev.com/hitchstory/using/alpha/steps-and-step-arguments)
- [Story that rewrites itself](https://hitchdev.com/hitchstory/using/alpha/rewrite-story)
- [Shortcut lookup for story names](https://hitchdev.com/hitchstory/using/alpha/shortcut-lookup)
- [Handling failing tests](https://hitchdev.com/hitchstory/using/alpha/failing-tests)
- [Continue on failure when playing multiple stories](https://hitchdev.com/hitchstory/using/alpha/continue-on-failure)
- [Play multiple stories in sequence](https://hitchdev.com/hitchstory/using/alpha/play-multiple-stories)
- [Variations](https://hitchdev.com/hitchstory/using/alpha/variations)
- [Flaky story detection](https://hitchdev.com/hitchstory/using/alpha/flaky-story-detection)
- [Generate documentation from stories](https://hitchdev.com/hitchstory/using/alpha/generate-documentation)
- [Gradual typing of story steps](https://hitchdev.com/hitchstory/using/alpha/gradual-typing)
- [Extra story metadata - e.g. adding JIRA ticket numbers to stories](https://hitchdev.com/hitchstory/using/alpha/metadata)
- [Given preconditions](https://hitchdev.com/hitchstory/using/alpha/given)
- [Hiding stacktraces for expected exceptions](https://hitchdev.com/hitchstory/using/alpha/expected-exceptions)
- [Special exception named failure](https://hitchdev.com/hitchstory/using/alpha/special-failure-exception)
- [Abort a story with ctrl-C](https://hitchdev.com/hitchstory/using/alpha/aborting)
- [Story with parameters](https://hitchdev.com/hitchstory/using/alpha/parameterized-stories)
- [Strong typing](https://hitchdev.com/hitchstory/using/alpha/strong-typing)
- [Running a single named story successfully](https://hitchdev.com/hitchstory/using/alpha/run-single-named-story)
- [Inherit one story from another](https://hitchdev.com/hitchstory/using/alpha/inheritance)



## Approach to using HitchStory

Best practices, how the tool was meant to be used, etc.

- [Recommended complementary tools](https://hitchdev.com/hitchstory/approach/complementary-tools)
- [Does hitchstory let your BA or Product Manager write stories while you just write the code?](https://hitchdev.com/hitchstory/approach/human-writable)
- [The importance of test realism](https://hitchdev.com/hitchstory/approach/test-realism)
- [Testing non-deterministic code](https://hitchdev.com/hitchstory/approach/testing-nondeterministic-code)
- [What is a testing and living documentation framework?](https://hitchdev.com/hitchstory/approach/testing-and-living-documentation)
- [Screenplay Principle](https://hitchdev.com/hitchstory/approach/screenplay-principle)
- [Tests are an investment](https://hitchdev.com/hitchstory/approach/test-investment)
- [Executable specifications](https://hitchdev.com/hitchstory/approach/executable-specifications)
- [Recommended Environment](https://hitchdev.com/hitchstory/approach/recommended-environment)
- [What is the difference betweeen a test and a story?](https://hitchdev.com/hitchstory/approach/test-or-story)
- [How can executable specifications and living documentation be used for stakeholder collaboration?](https://hitchdev.com/hitchstory/approach/stakeholder-collaboration)
- [Triality](https://hitchdev.com/hitchstory/approach/triality)
- [Flaky Tests](https://hitchdev.com/hitchstory/approach/flaky-tests)


## Design decisions and principles

Somewhat controversial design decisions are justified here.

- [Why programatically rewrite stories?](https://hitchdev.com/hitchstory/why/rewrite)
- [Why does hitchstory not have a command line interface?](https://hitchdev.com/hitchstory/why/no-cli)
- [Principles](https://hitchdev.com/hitchstory/why/principles)
- [Why does hitchstory mandate the use of given but not when and then?](https://hitchdev.com/hitchstory/why/given-when-then)
- [Why does HitchStory use StrictYAML?](https://hitchdev.com/hitchstory/why/strictyaml)
- [Why does hitchstory not have an opinion on what counts as interesting to "the business"?](https://hitchdev.com/hitchstory/why/interesting-to-the-business)
- [Why is inheritance a feature of hitchstory stories?](https://hitchdev.com/hitchstory/why/inheritance)
- [Declarative User Stories](https://hitchdev.com/hitchstory/why/declarative)
- [Two Unit Tests, Zero Integration Tests](https://hitchdev.com/hitchstory/why/2-unit-tests-0-integration-tests)


## Why not X instead?

There are several tools you can use instead, this is why you should use this one instead:

- [Why not use Behave, Lettuce or Cucumber (Gherkin)?](https://hitchdev.com/hitchstory/why-not/gherkin)
- [Why use hitchstory instead of a unit testing framework?](https://hitchdev.com/hitchstory/why-not/unit-test)
- [Why not use the Robot Framework?](https://hitchdev.com/hitchstory/why-not/robot)
