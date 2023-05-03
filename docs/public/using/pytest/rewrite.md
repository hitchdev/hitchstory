---
title: Self rewriting tests with pytest and hitchstory
---





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


## Rewrite story

By setting the environment variable REWRITE to "yes",
pytest can be configured to run tests in rewrite mode.

The only story configured to rewrite itself currently
is test_rewritable in test_other.py:





Running: `REWRITE=yes pytest -k test_rewritable test_other.py`

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





Running: `pytest -k test_failure test_other.py`

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

test_other.py:15: StoryFailure
----------------------------- Captured stdout call -----------------------------
Load web page at /login
=========================== short test summary info ============================
FAILED test_other.py::test_failure - hitchstory.exceptions.StoryFailure: RUNNING Failing story in /path/to/failure.story ... [[ RED ]][[ BRIGHT ]]FAILED in 0.1 seconds.[[ RESET ALL ]]

[[ BLUE ]]        website: /login  # preconditions
      steps:
    [[ BRIGHT ]]  - Failing step[[ NORMAL ]]
    [[ RESET ALL ]]

[[ RED ]][[ BRIGHT ]]hitchstory.exceptions.Failure[[ RESET ALL ]]
  [[ DIM ]][[ RED ]]
    Test failed.
    [[ RESET ALL ]]
[[ RED ]]This was not supposed to happen[[ RESET FORE ]]
======================= 1 failed, 1 deselected in 0.1s ========================
```







!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/pytest-rewrite.story">pytest-rewrite.story
    storytests.</a>

