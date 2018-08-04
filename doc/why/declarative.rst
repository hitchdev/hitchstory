Declarative User Stories
========================

HitchStory StoryFiles are declarative and not turing complete.

At their core, they essentially just contain marked up data - a set of preconditions (in 'given'),
a set of steps and arguments and the ability to parameterize the preconditions, step arguments
and inherit one story from another.

No loops. No if statements. Turing *in*completeness.

Using a less powerful language to write tests in sounds counter-intuitive. Surely you want
as much power as possible when writing tests so you can do as much as possible?

Except you don't want that power, because you don't need it, and if that power is there it
causes a few follow on problems:

* Technical debt

* Readability suffers

* You lose the ability to generate and process the data

This is a general principle of good code.
