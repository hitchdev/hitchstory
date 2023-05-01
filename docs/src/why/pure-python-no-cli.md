---
title: Why does HitchStory have no CLI runner - only a pure python API?
---

Most testing frameworks bundle a command line runner. For example,
with pytest you run the "pytest" command on the command line
followed by a set of switches. E.g.

```bash
pytest -s -k tests/test_linking.py
```

HitchStory provides just a pure python API, leaving the developer to re-use
an existing command line runner like [the skeleton default documented here](../../using/setup/basic-cli) or build their own.

There are three main reasons for this:


## 1. A command runner can still be copy and pasted

If you want a simple command line template to run hitchstory
tests you can copy and paste the example.



## 2. Trivial to embed within existing test framework

If you just want to dip your toe in the water - you can try writing a few
tests with hitchstory which run within your existing testing framework
(e.g. pytest) and reuse all of the tooling surrounding it.

An example of this is [documented here](../../using/setup/pytest).


## 3. For complex testing the flexibility of a Python API is more valuable

After dogfooding this framework for a long while, I have come to realize that
the requirements for running tests vary significantly and usually require
unique customization on a project specific basis. Examples include:

* Running the same set of tests under a new and an old version of python.
* Running tests against either a local version of the application or a deployed version.
* Running a large set of parameterized tests on a full run, others on a quick validation run.
* Orchestrating the tests from a different machine to the machine that the tests are run on, for parallelization purposes.

Some of these things can be achieved by writing bash scripts or plugins,
but the freedom 

