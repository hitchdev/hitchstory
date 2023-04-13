---
title: Separation of Test Concerns
---
# Separation of Test Concerns

Separation of Test Concerns is a form of [separation of concerns](https://en.wikipedia.org/wiki/Separation_of_concerns) where the user story of a test is described declaratively and kept entirely separate from the [turing complete](https://en.m.wikipedia.org/wiki/Turing_completeness) code (the "engine") that executes it.

It mirrors the separation of concerns exhibited by web applications adhering to the [MVC](https://en.m.wikipedia.org/wiki/Model–view–controller) pattern ([MTV](https://docs.djangoproject.com/en/2.1/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names) in the Django world).With hitchstory, an example of a non-turing complete, declarative user story would look something like this:

```yaml
Logged in as AzureDiamond:
  given:
    browser: firefox
  steps:
  - Visit: /login
  - Form filled:
      username: AzureDiamond
      password: hunter2
  - Click: login
  - Page should appear: dashboard
```

With corresponding engine code looking like this:

```python
    def form_filled(self, **textboxes):
        for name, contents in sorted(textboxes.items()):
            self.driver.fill_form(name, contents)

    def click(self, name):
        self.driver.click(name=name)
```


## xUnit tests : no separation of concerns

Unlike with hitchstory, xUnit tests do not have a layer to enforce separation test of concerns.

Nonetheless, a skilled developer can often read and derive the intended user story from code, especially if it is written clearly and is well commented. For example an equivalent to the above may be:

```python
def test_add_user(browser, web_server, init, dbsession):
    """Log in as AzureDiamond"""

    b = browser

    b.visit("http://localhost:8080/")

    b.find_by_css("#nav-admin").click()

    b.find_by_css("#btn-panel-login").click()

    b.fill("email", "AzureDiamond")
    b.fill("password", "hunter2")
    b.find_by_name("login").click()

    assert b.is_element_present_by_css("#nav-dash")
```

This isnt always the case, however, and it is very frequently the case that the intended behavior is difficult to derive from the test even for a skilled developer.




## No separation: less readable

Not all tests have an easily discernable specification. For example:

```python
    def test_edit_article_url_is_resolved(self):
        url = reverse('mumbles-api-articles:edit-article',args=['sOmE-iD'])
        self.assertEquals(resolve(url).func,edit_article)
```

This isnt a problem with the writer of the test - it is an intrinsic problem with xUnit tests. As they grow, they become more unreadable, and since they largely interact with code APIs the relevance to the overall app may be difficult to discern.




## Cucumber / Gherkin: Separation only between high level description and the rest

Cucumber (as well as its derivatives) is another framework that enforces a language layer, but instead of enforcing a separation between specification and execution it is shaped around creating a much less useful separation between high level specifications and the rest.

An example of such a high level scenario (drawn from a representative cucumber tutorial) is:

```gherkin
  Scenario: Create a new person
    Given API: I create a new person
    Then API: I check that POST call body is "OK"
    And API: I check that POST call status code is 200
```

This example exhibits [test concern leakage](../tests concerns-leakage).

This provides a limited window into the intended (or actual) behavior of the API as it is a very high level overview of the API's behavior. Key specification details about this story will still exist in this executable specification but they will be buried in the step code that the above translates to. 

Due to the need to bury key specification details (e.g. the contents of the API call creating the person), the step code will also have to be highly specialized and step code reusability will be inhibited.



