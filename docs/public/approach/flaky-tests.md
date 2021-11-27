---
title: Flaky Tests
---

Flaky tests are tests which will do not pass or fail consistently.

Higher level tests suffer more from flakiness than low level tests, although
this tends to be only because high level tests are testing more code.

The probability of flakiness increases with the amount of code being tested.

## How to deal with flakiness?

Extreme flakiness can lead to test failure habituation and, in extreme
cases, test abandonment.

Flakiness in any test should mainly be considered an undesirable property
to test for and, when detected, a bug to be fixed.

## Causes

There are a number of common causes of flaky tests:

* Timing issues
** The selenium sleep
* Dependencies behaving in unexpected ways:
** Upgraded packages
** New data from a downloaded database.
* Environment behaving in unexpected ways:
** Odd time
* Bugs and indeterminism in testing code
* Code that behaves non-deterministically

Flaky tests can almost always be solved through more:

* Increasing isolation
* Changing code to be deterministic
* Accomodating indeterminism

## Useful flakiness

Mostly test flakiness is just an irritation.

However, sometimes, flakiness is actually useful in that it highlights a
bug that would previously have remained uncovered.
