---
title: Using hitchstory with pytest
---



If you already have pytest set up and a full
suite of integration tests and would like to dip
your toe in the water with hitchstory, you
can easily run stories directly from inside pytest
without any plugins.

This example demonstrates the stories from the
README being run from inside pytest.




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
test_integration.py:

```python
from hitchstory import StoryCollection
from pathlib import Path
from engine import Engine

hs = StoryCollection(
    # All *.story files in this test's directory
    Path(__file__).parent.glob("*.story"), 
    Engine()
)

def test_email_sent():
    hs.named("Email sent").play()

def test_logged_in():
    hs.named("Logged in").play()
```





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






!!! note "Executable specification"

    Documentation automatically generated from 
    <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/story/pytest.story">pytest.story
    storytests.</a>

