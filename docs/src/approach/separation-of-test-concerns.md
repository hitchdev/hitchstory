---
title: Separation of Test Concerns
---
# Separation of Test Concerns

Separation of Test Concerns is a form of [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) where the user story is described declaratively and kept entirely separate from the turing complete code (the "engine") that executes it.

It mirrors the kind of separation of concerns exhibited by web applications adhering to the [MVC](https://en.m.wikipedia.org/wiki/Model–view–controller) pattern (or [MTV](https://docs.djangoproject.com/en/2.1/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names) as Django calls it).
With hitchstory, a declarative user story would look like this:

```yaml
Logged in as AzureDiamond:
  given:
    browser: firefox
  steps:
  - Visit: /login
  - Form filled:
      username: AzureDiamond
      password: hunter2
  - Clicked: login
  - Page should appear: dashboard
```

With corresponding test code looking like this:

```python
    def form_filled(self, **textboxes):
        for name, contents in sorted(textboxes.items()):
            self.driver.fill_form(name, contents)

    def clicked(self, name):
        self.driver.click(name=name)
```
Unlike with hitchstory, xUnit tests do not enforce any separation of concerns.

A skilled developer can often discern the user story from code, especially when it is relatively straightforward as follows:

```python
def test_add_user(browser, web_server, init, dbsession):
    """See that we can add new users."""

    b = browser

    create_logged_in_user(dbsession, init.config.registry, web_server, browser, admin=True)

    b.find_by_css("#nav-admin").click()

    b.find_by_css("#btn-panel-add-user").click()

    b.fill("email", "test2@example.com")
    b.fill("password", "secret")
    b.fill("password-confirm", "secret")
    b.find_by_name("add").click()

    # Convert to CSS based test
    assert b.is_element_present_by_css("#msg-item-added")
```
Not all tests have an easily discernable specification. For example:

```python
    def test_edit_article_url_is_resolved(self):
        url = reverse('mumbles-api-articles:edit-article',args=['sOmE-iD'])
        self.assertEquals(resolve(url).func,edit_article)
```

Part of the problem here is context. What does OmE-iD mean? Is it meaningful? What does it mean to resolve a URL?

This isnt a problem with the writer of the test - it is an intrinsic problem with xUnit tests. As they grow they become more unreadable.
Cucumber is another framework that enforces a language layer separation between specification. An example of such a readable high level test is:

```gherkin
  Scenario: Create a new person
    Given API: I create a new person
    Then API: I check that POST call body is "OK"
    And API: I check that POST call status code is 200
```

Cucumber succeeds in maintaining separation of concerns but fails in a number of other respects, all of which have led to it to struggle on fulfilling its core promise.
One common issue even with testing frameworks that enforce a separation of concerns is upward concern leakage.

This is where implementation details are "leaked" into the story, as is the case in this story where xpath selectors are included in the story:


```gherkin
  Scenario: Use select and deselect all buttons
    Given I log in as "teacher1"
    And I follow "Course 1"
    And I follow "Participants"
    When I press "Select all"
    Then the field with xpath "//tbody//tr[1]//input[@class='usercheckbox']" matches value "1"
    And the field with xpath "//tbody//tr[2]//input[@class='usercheckbox']" matches value "1"
```

Xpath selectors "pollute" the story.

This is not Cucumber's fault at all - it is a misuse of it. It is a potential problem with hitchstory as well.
Downward concern leakage is where elements of behavior are pushed down from the specification language to the code.

As an example:

```gherkin
  Scenario: Create a new person
    Given API: I create a new person
    Then API: I check that POST call body is "OK"
    And API: I check that POST call status code is 200
```

*How* a new person is created is left entirely open ended. Indeed, it's likely that there are many different ways that one could try to create a new person using an API that would not result in a status code of 200.

The step code used to exercise this story *is* precise about these things and the end user will certainly know what they are but it is left to the reader's imagination what they actually are.

Moreover the shape of the response that is available to the user is not shown.

This actually is cucumber's fault. There is no straightforward way to represent complex data.


