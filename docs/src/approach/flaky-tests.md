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

Some kinds of flakiness (e.g. race conditions) can be detected by running tests multiple times. A practical approach to doing this is documented in the [flaky story detection how to](../using/flaky-story-detection).

## Causes

There are a number of common different causes of flaky tests:

* Timing issues when interacting with interfaces (e.g. web pages on selenium)
** A common but very hacky fix for this is using sleeps. The "proper" way to fix this is with expected condition waits with timeouts.

* Dependencies behaving in unexpected ways:
** Upgraded packages in the test environment.
** New data from a downloaded database.

* Non deterministic code.
** SELECT statements without ORDER BY will often jumble the order of returned items, causing test failures 

* Bugs and indeterminism in testing code.

Flaky tests can almost always be solved through more:

* Increasing isolation - e.g. containerizing and upgrading containers consistently.
* Making code behave in a more deterministic fashion - e.g. always a LIMIT to all database select code.
* Accomodating indeterminism - making user stories accept the full range of potential outputs.

## Useful flakiness

Mostly test flakiness is just an irritation.

However, sometimes, flakiness is actually useful in that it highlights a
bug that would previously have remained uncovered - e.g. a race condition.
