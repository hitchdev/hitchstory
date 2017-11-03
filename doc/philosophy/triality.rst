Triality
========

All great software needs three things:

* Specification
* Tests
* Documentation

Each of these things is intimately tied. Every new feature must
be specified, tested and documented.

If each of these things are done separately, it violates another
core principle of software: DRY.

However, if each of these things are intrinsically the same -
the specification IS the test which IS the documentation, then
there is no need to duplicate effort, code and writing.

The idea of triality is that updating or adding to the specification
should intrinsically update tests and documentation with minimal
manual effort.

It is *not*, however, the idea that specification and documentation
are intrinsically the same thing:

* Not every edge case needs to be the basis of the documentation.
* Documentation need not be DRY - repetitive, fully fleshed out examples for all user stories are valuable to users who only wish to see one.
* Documentation can contain ancillary generated information that is not part of the spec but is seen when running it as a test - e.g. screenshots.
