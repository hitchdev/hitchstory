---
title: Flaky Tests
---

Flaky tests are tests which do not pass or fail consistently.

The probability of flakiness increases with the amount of code being tested. Extreme flakiness can lead to test failure habituation and, in extreme
cases, test abandonment.

Higher level tests suffer more from flakiness than low level tests, although
this tends to be only because high level tests are testing more code.

Flakiness in any test is an undesirable property.

## Detecting flakiness with HitchStory

Some kinds of flakiness (e.g. race conditions) can be detected by running tests multiple times.

## Causes

There are a number of common causes of flaky tests:

* Timing issues
** The selenium sleep is a hacky fix for this. Expected conditions waits are better.

* Dependencies behaving in unexpected ways:
** Upgraded packages in the test environment.
** New data from a downloaded database.

* Non deterministic code.
** SELECT statements without ORDER BY will often jumble the order of returned items, causing test failures 

* Environment behaving in unexpected ways:
* Bugs and indeterminism in testing code
* Code that behaves non-deterministically

Flaky tests can almost always be solved through more:

* Increasing isolation
* Making code more deterministic (e.g. 
* Accomodating indeterminism

## Useful flakiness

Mostly test flakiness is just an irritation.

However, sometimes, flakiness is actually useful in that it highlights a
bug that would previously have remained uncovered.
