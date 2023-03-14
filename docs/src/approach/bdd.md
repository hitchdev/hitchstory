---
title: Can I do BDD with hitchstory? How do I do BDD with hitchstory? 
---

Yes. BDD is a commonly misrepresented idea, however.

What it is often interpreted as is using Cucumber to write tests where "the business" may or may not (usually not) involve themselves in writing them.

What BDD actually is, is (much simplified):

1. A way to craft specifications using example written scenarios.
2. Using those scenarios to have conversations about intended behavior with stakeholders.
3. Using those scenarios as a way to agree example behavior.

That is, it's a way to evolve a program specification *only*. It doesn't require any tool. It can even in theory be done with pen and paper.

## Where does testing fit in to BDD?

Example based scenarios make extremely *good* acceptance tests. Once you use the results of a BDD specification to write a test with any tool, you are not doing BDD, you are probably doing ATDD (acceptance test driven development).

The two *can* be combined, saving time and repetition if, instead of pen and paper or short JIRA descriptions, you use a domain appropriate scenario language.

A language which can be used to execute tests *and* agree intended behavior with stakeholders can be used to combined BDD and ATDD.

## What is the combination of BDD and ATDD?

The combination of BDD and ATDD is executable specification driven development.

It requires the use of a domain appropriate scenario language.

## How does combining BDD and ATDD go wrong?

- Difficult to read scenario language. For example, if a program is largely tested with xUnit tests, even though the stakeholders will understand the scenarios they will usually not be able to read the tests.

- Inexpressive scenario language. A language that routinely abstracts away important details about the specification or ends up being very repetitive may be usable to write tests, but not to do do BDD. This is the most common failure mode with Gherkin/Cucumber tests due to their structure and syntax.

- Stakeholders are expected to want to write the scenario language. Drafting scenarios that are concise, clear and unambiguous is an art and a skill that most people do not have. It isn't programming, but it's more like programming than anything else.
