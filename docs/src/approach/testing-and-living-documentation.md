---
title: What is a testing and living documentation framework?
---

While traditional testing frameworks are designed *just* to test code and find bugs,
hitchstory is designed such that the "tests" you write are example specifications which can be [executed and used to generate how to documentation](../triality).

[xUnit](https://en.wikipedia.org/wiki/XUnit) testing frameworks like pytest do not allow for this because there is [no clear separation of concerns](../separation-of-test-concerns) between specification and execution code. At best they can sometimes serve as [documentation for somebody who knows how to read them](https://capgemini.github.io/development/unit-tests-as-documentation/).

## What is the difference between an executable specification and living documentation?

While executable specifications are typically a lot clearer and easier to understand
than xUnit test code, the qualities of good executable specifications still conflict
with the qualities of good documentation.



. Moreover, it can be used for effective [stakeholder collaboration](../stakeholder-collaboration),
especially with highly technical stakeholders.

However, hitchstory takes the approach that documentation and specification
are two very closely related but highly *distinct* things and that instead of
treating them as one and the same, that the best documentation is built from a
combination of skeleton docs, executable specifications and (sometimes) test
artefacts.

## Why do you want executable specifications and documentation to be separate?

Good executable specifications are terse, DRY and highly specific and
follow the [screenplay principle](../screenplay-principle) but that doesn't
make the best documentation.

Good documentation, on the other hand, should *not* be terse or DRY. Moreover,
stakeholders are usually interested only in certain aspects of how the application
behaves. A lot of them will not care about the really obscure edge cases you have
to program in, for example and feeding them details which do not matter to
them will not just bore them, it will lead to them skimming and missing
the really important details that matter to them.

## Who is the documentation for?

A CEO, translator, product manager, customer, designer, UX, third party
API consumer/producer, etc. are all interested in different details of how
your software behaves and they will have varying levels of interest in the
level of detail about your software's behavior.

It may even make sense for some projects to generate more than one kind of
documentation for different kinds of stakeholders from the same specifications
albeit varying levels of detail - or, at the very least, documentation which
can expose high level details of the software on top and detail that can be
drilled down into.
