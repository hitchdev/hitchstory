---
title: Does hitchstory let your BA or Product Manager write stories while you just write the code?
---

It is possible but I wouldn't necessarily recommend it.

Having "analysts" write and read stories instead of programmers was an explicit goal
of several BDD tools like cucumber. However, the reality of these tools is that
"the business" is not often interested in reading these stories, let alone writing
them.

This is an explicit non-goal of hitchstory. The framework is designed to be useful
even if it is *solely* used by developers. Indeed, if your product manager/owner/designated
troll shows no interest at all that's okay.

## Story maintenance and writing is a bit like programming

Well maintained stories will typically be readable and comprehensible by non-programmers
with a good knowledge of the domain (unlike code), but they will likely not be very
good at writing or maintaining [high quality stories](../good-stories) - at least,
not without training.

That said, *pairing* with business analysts while writing and maintaining stories,
especially on an ad hoc basis can be a supremely effective workflow for doing
[stakeholder collaboration](../stakeholder-collaboration).

## What about QA?

While developers need to be involved in writing the stories, the developers
primarily writing the stories need not necessarily be the developers writing
the application. The stories do not even have to bet written in the same
language.

[ TODO : Where to surround the story ]
