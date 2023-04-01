---
title: What is a testing and living documentation framework?
---

While traditional testing frameworks are designed *just* to test code and find bugs,
hitchstory is designed such that the "tests" you write are example specifications which can be [executed and used to generate how to documentation](../triality).

[xUnit](https://en.wikipedia.org/wiki/XUnit) testing frameworks like pytest do not allow for this because there is [no clear separation of concerns](../separation-of-test-concerns) between specification and execution code. At best they can sometimes serve as [documentation for somebody who knows how to read them](https://capgemini.github.io/development/unit-tests-as-documentation/).

## What is the difference between an executable specification and living documentation?

While executable specifications are typically a lot clearer and easier to understand
than xUnit test code, the qualities of good executable specifications still conflict
with the qualities of good documentation.

Good executable specification are:

* Terse
* DRY
* Will assume most relevant domain knowledge
* Covers edge cases

Whereas clear documentation:

* Is expansive, not terse
* Is not DRY
* Does not necessarily assume domain knowledge
* Will not cover most edge cases

## "Business readable" documentation

Cucumber's official documentation takes the opinion that [business readable specs](https://cucumber.io/blog/bdd/isn-t-the-business-readable-documentation-just-ove/) are worthwhile to maintain and it is true.

However, while all stakeholders have some kind of interest in the behavior of the software, they will all have wildly varying levels of interest in the detail.

Cucumber's approach is to provide a high level human-language-like interface to low
level code, where the onus is on the developer to depict a level of detail that is "just right" for "the business". As an example:

```gherkin
  Scenario: Create a new person
    Given API: I create a new person
    Then API: I check that POST call body is "OK"
    And API: I check that POST call status code is 200
```

Since the syntax of Gherkin is not suitable for representing complex specifications and many key details *are* uninteresting to stakeholders, key details often get pushed down to the execution layer. This can end up with details the business *is* interested in (e.g. how the new person is created) being concealed while uninteresting details (e.g. 200 status code) are surfaced.

HitchStory takes the approach that *no* specification details should be buried in the
execution layer and what is "interesting to stakeholders" is a matter for whomever is
implementing the documentation generation step to worry about.


