---
title: Why does HitchStory have no CLI runner - only a pure python API?
---

HitchStory aims to be usable as both as a self-contained library running
within pytest or on its own via a custom made runner.

There are three reasons for this:


## 1. Easy integration with pytest

Most people already use pytest as a test runner. The pure python
API makes it easy to integrate hitchstory with it.

## 2. It's still easy to create a command line runner if you like

The [the skeleton runner is documented here](../../using/setup/basic-cli)
if you'd prefer not to use pytest.


## 2. For complex test strategies the flexibility of a Python API is very valuable

After dogfooding this framework for a long while, I have come to realize that
the requirements for running tests vary significantly and usually require
unique customization on a project specific basis. Examples include:

* Running the same set of tests under a new and an old version of python.
* Running tests against either a local version of the application or a deployed version.
* Running a large set of parameterized tests on a full run, others on a quick validation run.
* Orchestrating the tests from a different machine to the machine that the tests are run on, for parallelization purposes.

Some of these things can be achieved by writing bash scripts or plugins,
but python still gives you more options to customize.

