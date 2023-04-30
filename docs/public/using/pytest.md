---
title: Using hitchstory with pytest
---



If you already have pytest set up and a full
suite of integration tests and would like to dip
your toe in the water with hitchstory, you
can easily run stories directly from inside pytest.

The following files - engine.py, the .story files
can all be put in the same folder.




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
from hitchstory import BaseEngine, GivenDefinition, GivenProperty, Failure
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
    
    def error_message_displayed(self, message):
        pass

    def email_was_sent(self):
        email_was_sent()
```
failure.story:

```yaml
Failing story:
  given:
    website: /login  # preconditions
  steps:
  - Failing step
```
test_failure.py:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine
import os

hs = StoryCollection(
    # All *.story files in this test's directory
    Path(__file__).parent.glob("*.story"), 
    Engine(rewrite=os.getenv("REWRITE", "") == "yes")
).with_external_test_runner()

def test_failure():
    hs.named("Failing story").play()
```
test_integration.py:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine

hs = StoryCollection(
    # All *.story files in this test's directory
    Path(__file__).parent.glob("*.story"), 
    Engine()
).with_external_test_runner()

def test_email_sent():
    hs.named("Email sent").play()

def test_logged_in():
    hs.named("Logged in").play()
```




## Run all tests






Running: `pytest test_integration.py`

Outputs:
```
============================= test session starts ==============================
platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
rootdir: /path/to
collected 2 items

test_integration.py ..                                                   [100%]

============================== 2 passed in 0.1s ===============================
```


## Failing test






Running: `pytest test_failure.py`

Outputs:
```
============================= test session starts ==============================
platform linux -- Python n.n.n, pytest-n.n.n, pluggy-n.n.n
rootdir: /path/to
collected 1 item

test_failure.py F                                                        [100%]

=================================== FAILURES ===================================
_________________________________ test_failure _________________________________

    def test_failure():
>       hs.named("Failing story").play()
E       hitchstory.exceptions.StoryFailure: RUNNING Failing story in /path/to/failure.story ... [[ RED ]][[ BRIGHT ]]FAILED in 0.1 seconds.[[ RESET ALL ]]
E
E       [[ BLUE ]]        website: /login  # preconditions
E             steps:
E           [[ BRIGHT ]]  - Failing step[[ NORMAL ]]
E           [[ RESET ALL ]]
E
E       [[ RED ]][[ BRIGHT ]]hitchstory.exceptions.Failure[[ RESET ALL ]]
E         [[ DIM ]][[ RED ]]
E           Test failed.
E           [[ RESET ALL ]]
E       [[ RED ]]This was not supposed to happen[[ RESET FORE ]]

test_failure.py:13: StoryFailure
----------------------------- Captured stdout call -----------------------------

Visiting http://localhost:5000/login
=========================== short test summary info ============================
FAILED test_failure.py::test_failure - hitchstory.exceptions.StoryFailure: RUNNING Failing story in /path/to/failure.story ... [[ RED ]][[ BRIGHT ]]FAILED in 0.1 seconds.[[ RESET ALL ]]

[[ BLUE ]]        website: /login  # preconditions
      steps:
    [[ BRIGHT ]]  - Failing step[[ NORMAL ]]
    [[ RESET ALL ]]

[[ RED ]][[ BRIGHT ]]hitchstory.exceptions.Failure[[ RESET ALL ]]
  [[ DIM ]][[ RED ]]
    Test failed.
    [[ RESET ALL ]]
[[ RED ]]This was not supposed to happen[[ RESET FORE ]]
============================== 1 failed in 0.1s ===============================
```







!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/pytest.story">pytest.story
    storytests.</a>

