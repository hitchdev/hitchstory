---
title: Principles
---

This library was dogfooded for years to TDD / BDD, test and autodocument a variety
of different kinds of software - web apps, python libraries, command line apps,
replacing all other forms of unit, integration and end to end tests.

Unlike traditional "BDD" frameworks like Cucumber, hitchstory is not primarily designed for
"[business readability](https://www.martinfowler.com/bliki/BusinessReadableDSL.html)",
but rather for simplicity ease of maintenance by developers.

This means:

* Stories can *and should* inherit from one another, because *specifications ought to be DRY too*.
* Stories are defined and validated using strongly typed StrictYAML. Step arguments and precondition ('given') schemas can be strictly defined by the programmer.
* The execution engine can be programmed to rewrite the executing story based upon certain kinds of behavior changes (e.g. output strings, screen output changes, messages in a web app).
* Running stories is done via a python API rather than the command line so you can easily program customized test workflows.
* There is built  in story parameterization so you can do property based testing.
* Stories can be easily tested for flakiness.
* The stories are designed to be easily used to build readable documentation.
