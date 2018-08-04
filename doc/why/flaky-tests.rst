Flaky Tests
===========

Flaky tests are tests which will do not pass or fail consistently.

Higher level tests suffer more from flakiness than low level tests, although
this tends to be only because high level tests are testing more, which increases
the probability of flakiness.

Flakiness in any test should be considered a *bug to be fixed*.

It should not ever, *ever* just be considered "just a fact of life". That's bad
engineering.

It should not ever be considered a reason to choose lower level testing over
higher level testing.

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

Flaky tests can be solved with an approach known as radical isolation.

Useful flakiness
----------------

Mostly test flakiness is just an irritation.

However, sometimes, flakiness is actually useful in that it highlights a
bug that would previously have remained uncovered.

Examples:

e

Theoretically you should be celebrating because you've efficiently caught
a bug in both your test code and your application code. Realistically,
you've just added three tasks to your plate:

* Fixing the test to prevent it from being
