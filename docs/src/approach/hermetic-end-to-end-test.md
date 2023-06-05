---
title: The Hermetic End to End Testing Pattern
---
# The Hermetic End to End Testing Pattern

The hermetic end to end testing pattern is a pattern where:

* The entire app is run as a cohesive whole.

* The entire "outside world" for this app is run in a strictly controlled mock environment. For example, if it:

** Calls an external sandbox REST API.
** Uses a staging database whose exact data isn't controlled.
** Accesses the the internet.

Then it is not hermetic. If it:

** Calls a mock REST API (e.g. using wiremock or mitmproxy).
** Uses a locally built database with consistent pre-defined fixtures.
** Doesn't access the internet.

Then it is hermetic.

## Benefits

Hermetic tests are:

* Faster.
* More consistent.
* Trivially parallelizable

## Partially hermetic end to end tests

Partial hermeticism is when every part of the end to end test is mocked, but it can be run in a mode that partially interacts with the outside world.

An example of this would be a hermetic end to end test that calls a mocked Paypal REST API using wiremock or mitmprox, but which can be run in a mode that uses the sandboxed Paypal REST API instead.

Partial hermeticism can be used as:

* An efficient way of creating mocks (by recording the actual request / response).
* A way of consistently testing "outside world" changes - e.g. if an API the app calls still works the same way tomorrow as it did yesterday.


## Further reading

* [Google Testing Blog](https://testing.googleblog.com/2012/10/hermetic-servers.html)
* [My Recent Obsession with Hermetic Tests](https://blog.testproject.io/2021/09/13/my-recent-obsession-with-hermetic-tests/)
* [Hermetic Unit Testing](https://medium.com/geekculture/hermetic-unit-testing-8c49276e3acd)
* [TestContainers](https://www.testcontainers.org/)
