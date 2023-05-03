---
title: Dip your toe in the water with pytest
---



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
  
See James' analytics:
  based on: log in as james  # inheritance
  following steps:
  - Click: analytics
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
test_hitchstory.py:

```python
from hitchstory import BaseEngine, GivenDefinition, GivenProperty
from hitchstory import Failure, strings_match
from hitchstory import StoryCollection
from pathlib import Path
from strictyaml import Str
import os

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


hs = StoryCollection(
    # All *.story files in test_hitchstory.py's directory
    Path(__file__).parent.glob("*.story"),
    
    # If REWRITE environment variable is set to yes -> rewrite mode.
    Engine(rewrite=os.getenv("REWRITE", "") == "yes")
).with_external_test_runner()

def test_log_in_as_james():
    hs.named("Log in as james").play()

def test_see_james_analytics():
    hs.named("See James' analytics").play()
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

    def test_see_james_analytics():
>       hs.named("See James' analytics").play()
E       hitchstory.exceptions.StoryFailure: RUNNING See James' analytics in /path/to/example.story ... [[ RED ]][[ BRIGHT ]]FAILED in 0.1 seconds.[[ RESET ALL ]]
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

test_hitchstory.py:47: StoryFailure
----------------------------- Captured stdout call -----------------------------
Using browser firefox
Enter james in username
Enter password in password
Click on log in
Click on analytics
=========================== short test summary info ============================
FAILED test_hitchstory.py::test_see_james_analytics - hitchstory.exceptions.StoryFailure: RUNNING See James' analytics in /path/to/example.story ... [[ RED ]][[ BRIGHT ]]FAILED in 0.1 seconds.[[ RESET ALL ]]

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







!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/pytest.story">pytest.story
    storytests.</a>

