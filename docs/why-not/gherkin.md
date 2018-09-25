---
title: Differences to Gherkin
---

HitchStory and Gherkin are both DSLs for writing user stories that can double as
acceptance tests, but they have different philosophies and approach.

Gherkin scenarios emphasize the following values:

* The use of English to facilitate customer collaboration.
* Showing information that is "interesting to the business".

Here are some examples.

From the Cucumber website:

```gherkin
Scenario: Buy last coffee
  Given there are 1 coffees left in the machine
  And I have deposited 1$
  When I press the coffee button
  Then I should be served a coffee
```

Hitch scenarios, by contrast, emphasizes the following values:

* Ease of use and maintenance by developers first.
* The screenplay principle.
* Terse, DRY code.
* The generation of documentation for customer collaboration and stakeholders input from specifications.

Equivalent scenarios:

```yaml
Buy last coffee:
  given:
    machine contains:
      coffees: 1
  steps:
  - Deposit: $1
  - Press button: coffee
  - Served up: coffee
```
