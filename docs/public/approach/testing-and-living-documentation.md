---
title: What is a testing and living documentation framework?
---

While traditional testing frameworks are designed *just* to test code and find bugs,
hitchstory is designed such that the "tests" you write can *also* be used as
specifications that define how your application is supposed to work.

The three critical features that let you do this are:

* A clear separation of concerns between specification and execution code
* A clear segregation barrier between the environment that *executes* your tests and the environment *under* test.
* The executable specifications are described using declarative markup instead of turing complete code

Most tests - *especially* unit tests - fail on all three counts and the code ends up
being smush of obscure mocks, combined with unclear scenarios and no explanation why
any part of it does anything that it does.

Writing tests that double as [executable specifications](../executable-specifications)
makes these tests useful not only as a kind of pseudo-documentation, but also as a
template that can be used to generate living documentation.

## What is the difference between an executable specification and living documentation?

I dubbed a specification "pseudo documentation" above, because  executable specifications
are already a *hell* of a lot clearer and easier to understand
than most test code. Moreover, it can be used for effective [stakeholder collaboration](../stakeholder-collaboration),
especially with highly technical stakeholders.

However, hitchstory takes the approach that documentation and specification
are two very closely related but highly *distinct* things and that instead of
treating them as one and the same, that the best documentation is built from a
combination of skeleton docs, executable specifications and (sometimes) test
artefacts.

## What's a good executable specification? What is good documentation?

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
