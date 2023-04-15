---
title: Test Artefact Environment Isolation
---
# Test Artefact Environment Isolation

Test-Artefact Environment Isolation is a capability of some tests where:

- The environment running test code is kept in a strictly segregated environment from the artefact or code under test.
- The artefact under test is built to mimic as closely as possible the artefact that will run in production.

It is a property of some (but not all) integration tests and is a capability that when built out can aid with effective [shift left testing](https://en.wikipedia.org/wiki/Shift-left_testing).


## How can a lack of isolation hurt?

I built some tests once that ran a scenario that roughly followed this process:

- Log in to the website
- Upload some image
- An image transformation was applied
- That transformed image was then displayed

The integration tests ran a lot of examples with transformations that worked fine and produced expected outputs. Some cursory manual testing of the app deployed on staging also showed no problems.

However, once the release went out a number of reports of ruined images started coming from users.

These issues were *not* reproducible with the integration tests.

With the integration tests running the same code on the the same images that came out ruined looked just fine.

The problem, as it turned out, was caused by an interaction between the image transformation library and a particular version of a system library it depended upon. This problem wasnt present in the container used for integration testing because the dependencies of the testing code "fixed" the problem.

For many developers it is considered a normal practice to run tests and artefact within the same environment, so variations on this class of bug are not uncommon.




## Isolation in practice

In the above example, isolation was achieved by separating out the test code into an entirely separate docker container.

This container ran the artefact container and directly interacted with it. The artefact could then be built to resemble the container run in production but still be run on a local machine or in CI.




## HitchStory

HitchStory doesn't have to be used this way but was built with the presumption that it would be used with test artefact environment isolation.

Even the storytests it uses to test itself follow this principle, as do the storytests written to test strictyaml.

(coming soon : example API tests, playwright tests demonstrating test-artefact environment isolation)




## Isolation vs Speed

Isolation comes at a price, and that price is often speed.

A test that runs a test with a real against a real container running a real web server and database will naturally start up and run a lot slower than a test that hooks in at a lower layer (typically dubbed "[subcutaneous testing](https://www.martinfowler.com/bliki/SubcutaneousTest.html)") and uses speedier mocks (e.g. sqlite instead of postgres).

For many types of code, this lack of environmental parity between test and prod doesnt cause problems.

Indeed, especially for highly complex and self contained calculation code (the kind of code where unit tests tend to shine), the overhead of maintaining test artefact environment isolation may far outweigh the benefits.

Where isolation will be most beneficial will be for integration tests on code that involves complex integration.



