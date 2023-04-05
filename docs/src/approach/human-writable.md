---
title: Does hitchstory let "the business" write stories while you just write the code?
---

Having "analysts" write and read stories instead of programmers was an explicit goal of several BDD tools like Cucumber. However, the reality of these tools is that "the business" is rarely interested in reading these stories, let alone writing them.

This is an explicit non-goal of hitchstory. The framework is designed such that
it does not have loops, conditionals or other such accoutrements of a programming
language and *could* be written by a sophisticated product manager, but it is
still a tool squarely aimed at developers.

## Story maintenance and writing is a bit like programming

Well maintained stories will typically be readable and comprehensible by non-programmers
with a good knowledge of the domain (unlike code), but they will likely not be very
good at writing or maintaining high quality stories - at least,
not without prior training.

That said, *pairing* with business analysts while writing and maintaining stories,
especially on an ad hoc basis can be a supremely effective workflow for doing
[stakeholder collaboration](../bdd).


## Should testers write stories?

While developers need to be involved in writing the stories, the developers
primarily writing the stories need not necessarily be the developers writing
the application. The stories do not even have to be written in the same
language.
