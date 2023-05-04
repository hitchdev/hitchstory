---
title: Self rewriting tests with pytest and hitchstory
---





# Code Example



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
failure.story:

```yaml
Failing story:
  given:
    website: /login  # preconditions
  steps:
  - Failing step
```
rewritable.story:

```yaml
Rewritable story:
  given:
    website: /error
  steps:
  - Error message displayed: old message
```
test_integration.py:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine
import os

hs = StoryCollection(
    # All *.story files in this test's directory
    Path(__file__).parent.glob("*.story"),
    
    # Rewrite if REWRITE environment variable is set to yes
    Engine(rewrite=os.getenv("REWRITE", "") == "yes")
).with_external_test_runner()

def test_email_sent():
    hs.named("Email sent").play()

def test_logged_in():
    hs.named("Logged in").play()
    
```
test_other.py:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine
import os

hs = StoryCollection(
    # All *.story files in this test's directory
    Path(__file__).parent.glob("*.story"),

    # Rewrite if REWRITE environment variable is set to yes
    Engine(rewrite=os.getenv("REWRITE", "") == "yes")
).with_external_test_runner()

def test_failure():
    hs.named("Failing story").play()

def test_rewritable():
    hs.named("Rewritable story").play()
```




## Run all passing tests

This runs the two tests in test_integration.py.





`pytest test_integration.py`

Outputs:
```
============================= test session starts ==============================
platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
rootdir: /path/to
collected 2 items

test_integration.py ..                                                   [100%]

============================== 2 passed in 0.1s ===============================
```


## Rewrite story

By setting the environment variable REWRITE to "yes",
pytest can be configured to run tests in rewrite mode.

The only story configured to rewrite itself currently
is test_rewritable in test_other.py:





`REWRITE=yes pytest -k test_rewritable test_other.py`

Outputs:
```
============================= test session starts ==============================
platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
rootdir: /path/to
collected 2 items / 1 deselected / 1 selected

test_other.py .                                                          [100%]

======================= 1 passed, 1 deselected in 0.1s ========================
```

File rewritable.story should now contain:

```
Rewritable story:
  given:
    website: /error
  steps:
  - Error message displayed: error message!
```


## Failing test

Failing tests will result in a StoryFailure exception being
raised.

The message within the exception will contain details of the
step where the test failed.

For most exceptions (not this one), there will be a stack
trace displayed as well.

Note that the [[ COLOR ]] will be replaced with actual colors
if this is run on the command line.





`pytest -k test_failure test_other.py`

Outputs:
```
============================= test session starts ==============================
platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
rootdir: /path/to
collected 2 items / 1 deselected / 1 selected

test_other.py F                                                          [100%]

=================================== FAILURES ===================================
_________________________________ test_failure _________________________________

    def test_failure():
>       hs.named("Failing story").play()
E       hitchstory.exceptions.StoryFailure: RUNNING Failing story in /path/to/failure.story ... FAILED in 0.1 seconds.
E
E               website: /login  # preconditions
E             steps:
E             - Failing step
E
E
E       hitchstory.exceptions.Failure
E
E           Test failed.
E
E       This was not supposed to happen

test_other.py:15: StoryFailure
----------------------------- Captured stdout call -----------------------------
Load web page at /login
=========================== short test summary info ============================
FAILED test_other.py::test_failure - hitchstory.exceptions.StoryFailure: RUNNING Failing story in /path/to/failure.story ... FAILED in 0.1 seconds.

        website: /login  # preconditions
      steps:
      - Failing step


hitchstory.exceptions.Failure

    Test failed.

This was not supposed to happen
======================= 1 failed, 1 deselected in 0.1s ========================
```







!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/pytest-rewrite.story">pytest-rewrite.story
    storytests.</a>

