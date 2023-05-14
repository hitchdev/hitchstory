---
title: Is HitchStory a BDD tool? How do I do BDD with hitchstory? 
---

BDD has two meanings. I believe that they conflict:

* Writing Gherkin and executing Gherkin - like Cucumber, Behave, RSpec.
* A tool that can be used for stakeholder collaboration.

A large part of my motivation for building hitchstory was:

1. I believed in writing a tool **primarily** integration testers to write integration tests.

2. I believed that Gherkin made stakeholder collaboration harder, and I wanted to make it easier.

BDD is a commonly misrepresented idea. It was always intrinsically linked to Gherkin in people's minds but it was never about Gherkin.

What BDD actually is, is:

1. A way to craft specifications using example written scenarios.
2. Using those scenarios to have *conversations* about intended behavior with stakeholders.
3. Using those scenarios as a way to agree example behavior.

That is, it's a way to evolve a program specification *only*. It never required any tool. **It could be done on the back of a napkin**.


## Where does testing fit in to BDD?

Example based scenarios make extremely *good* acceptance tests. Once you use the results of a BDD specification to write a test with any tool, you are not doing BDD, you are probably doing ATDD (acceptance test driven development).

The two *can* be combined, saving time and repetition if, instead of pen and paper or short JIRA descriptions, you use a domain appropriate scenario language.

A language which can be used to execute tests *and* agree intended behavior with stakeholders can be used to combine BDD and ATDD.

## How does combining BDD and ATDD go wrong?S

With Gherkin, I think it usually did.

- If you used a difficult to read scenario language. For example, if a program is largely tested with xUnit tests, even though the stakeholders will understand the scenarios they will usually not be able to read the tests.

- Inexpressive scenario language. A language that routinely abstracts away important details about the specification or ends up being very repetitive may be usable to write tests, but not to do do BDD. This is the most common failure mode with Gherkin/Cucumber tests due to their structure and syntax.

- Stakeholders are expected to want to write the scenario language. Drafting scenarios that are concise, clear and unambiguous is an art and a skill that most people do not have. It isn't programming, but it's more like programming than anything else.
