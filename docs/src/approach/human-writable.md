---
title: ANTIPATTERN - Analysts writing stories for the developer
---

>Gherkin allows Business Analysts to document acceptance tests in a language developers, QA & the business can understand (i.e. the language of Gherkin). By having a common language to describe acceptance tests, it encourages collaboration and a common understanding of the tests being run. - [Gherkin for business analysts](https://www.modernanalyst.com/Resources/Articles/tabid/115/ID/3810/Gherkin-for-Business-Analysts.aspx)

Having analysts write and read stories instead of programmers was an explicit goal of most BDD tools like Cucumber. This was an enticing prospect - the developer wouldn't have to write tests (what a chore!). The product owner 

However, the reality of these tools is that stakeholders are interested in even reading these stories, let alone writing them.

This is an explicit non-goal of hitchstory. The framework is designed such that it does not have loops, conditionals or other such accoutrements of a programming language and *could* be written by a sophisticated product manager, but it is still a tool squarely aimed at developers.

## Story maintenance and writing is a bit like programming

Well maintained stories will typically be readable and comprehensible by non-programmers with a good knowledge of the domain (unlike code), but they will likely not be very good at writing or maintaining high quality stories - at least, not without prior training.

That said, *pairing* with business analysts while writing and maintaining stories, especially on an ad hoc basis can be a supremely effective workflow for doing [stakeholder collaboration](../bdd).


## Should testers write stories?

While developers need to be involved in writing the stories, the developers primarily writing the stories need not necessarily be the developers writing the application.
