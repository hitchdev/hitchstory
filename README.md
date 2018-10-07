# HitchStory


HitchStory is a python 3 library for creating readable "specifications by example" and executing
them. It is an ambitious project intended supplant both traditional BDD tools and unit tests.

Unlike many other BDD tools the specification is [written using StrictYAML](https://hitchdev.com/hitchstory/why/strictyaml) which
means that stories will be terse, strongly typed and expressive enough to describe business
rules and behavior in precise detail.


## Example








example.story:

```yaml
Log in:
  given:
    website: /login                  # preconditions
  steps:
    - Fill form:
        username: AzureDiamond       # parameterized steps
        password: hunter2
    - Click: login


Send email:
  about: Core functionality of app.
  based on: log in                 # inherits from and continues from test above
  steps:
    - Click: new email
    - Fill form:
        to: Cthon98@aol.com
        contents: |                # long form text
          Hey guys,

          I think I got hacked!
    - Click: send email
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

    def fill_form(self, **textboxes):
        for name, contents in sorted(textboxes.items()):
            self.driver.fill_form(name, contents)

    def click(self, name):
        self.driver.click(name)

    def email_was_sent(self):
        email_was_sent()

```









```python
from hitchstory import StoryCollection
from pathquery import pathquery
from engine import Engine

StoryCollection(pathquery(".").ext("story"), Engine()).named("Send email").play()

```

Will output:
```
RUNNING Send email in /path/to/example.story ...
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












## Installing

It's recommended to install and [set up hitchstory with hitchkey](https://hitchdev.com/hitchstory/setup-with-hitchkey), which can take care of automatically
setting up a up the [recommended hitchstory environment](https://hitchdev.com/hitchstory/approach/recommended-environment).

You can also install it traditionally through pypi:

```bash
$ pip install hitchstory
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
- [Screenplay Principle](https://hitchdev.com/hitchstory/approach/screenplay-principle)
- [Can I do BDD with hitchstory? How do I do BDD with hitchstory?](https://hitchdev.com/hitchstory/approach/bdd)
- [Recommended Environment](https://hitchdev.com/hitchstory/approach/recommended-environment)
- [What is the difference betweeen a test and a story?](https://hitchdev.com/hitchstory/approach/test-or-story)
- [Triality](https://hitchdev.com/hitchstory/approach/triality)
- [Flaky Tests](https://hitchdev.com/hitchstory/approach/flaky-tests)


## Design decisions and principles

Somewhat controversial design decisions are justified here.

- [Principles](https://hitchdev.com/hitchstory/why/principles)
- [I see given but where is when and then?](https://hitchdev.com/hitchstory/why/given-when-then)
- [Why does HitchStory use StrictYAML?](https://hitchdev.com/hitchstory/why/strictyaml)
- [Why does hitchstory not have an opinion on what counts as interesting to "the business"?](https://hitchdev.com/hitchstory/why/interesting-to-the-business)
- [Discussion of requested feature inheritance in Cucumber](https://hitchdev.com/hitchstory/why/inheritance)
- [Declarative User Stories](https://hitchdev.com/hitchstory/why/declarative)
- [Two Unit Tests, Zero Integration Tests](https://hitchdev.com/hitchstory/why/2-unit-tests-0-integration-tests)


## Why not X instead?

There are several tools you can use instead, this is why you should use this one instead:

- [Why not use Behave, Lettuce or Cucumber (Gherkin)?](https://hitchdev.com/hitchstory/why-not/gherkin)
- [Why use hitchstory instead of a unit testing framework?](https://hitchdev.com/hitchstory/why-not/unit-test)
- [Why not use the Robot Framework?](https://hitchdev.com/hitchstory/why-not/robot)
