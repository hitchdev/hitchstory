---
title: Flaky Tests
---

Flaky tests are tests which will do not pass or fail consistently.

Higher level tests suffer more from flakiness than low level tests, although
this tends to be only because high level tests are testing more code.

The probability of flakiness increases with the amount of code being tested.

How to deal with flakiness?
---------------------------

Flakiness in any test should be considered a *bug to be fixed*.

It should not ever, *ever* just be considered "just a fact of life". That's bad
engineering.

It should not be considered a reason to choose lower level testing over
higher level testing either.s

Extreme flakiness can lead to test failure habituation and, in extreme
cases, test abandonment.

Causes
------

There are a number of common causes of flaky tests:

* Timing issues
** The selenium sleep
* Dependencies and environment behaving in unexpected ways:
** Odd time
** Upgraded packages
** New data from a downloaded database.
* Bugs in testing code
* Code that behaves non-deterministically

Flaky tests can be solved with an approach known as radical isolation.

Useful flakiness
----------------

Mostly test flakiness is just an irritation.

However, sometimes, flakiness is actually useful in that it highlights a
bug that would previously have remained uncovered.

Regression flakiness
--------------------

TODO : implement feature that runs regression tests that only test
that for flakiness.
