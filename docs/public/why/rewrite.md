---
title: Why Rewritable Test Driven Development (RTDD)?
---

Rewritable test driven development is a form of test driven development
where the developer changes some code, runs a test in rewrite mode
and the test runner *rewrites* the test to match the changed output.

A hitchstory test rewriting itself after a code change:

1. The test is run with the old text - "To-do list" and *passes*.
2. The code is tweaked to say "My to-do list".
3. The test is run in normal mode and FAILS.
5. The test is run in rewrite mode and *PASSES*, rewriting the test.
6. The test is changed and PASSES when run in normal mode.

[![Test rewriting itself](https://hitchdev.com/images/video-thumb.png)](https://vimeo.com/822561823 "Test rewriting itself")

!!! note "Some coding"

    The video also demonstrates how to adjust the engine to make the test rewrite.

## Why do it?

Traditional test driven development implores you to construct a test first
and write the code that makes it pass after.

Where a desired output is trivial to validate at a glance but tedious
to construct, this is a waste of time. It is far better to let the
testing framework take care of it for you and to read the rewritten
test before committing.

This technique is particularly useful for integration tests that validate:

* Exact messages displayed on a website.
* REST API responses
* The output of command line applications


## When *not* to use it?

This technique must ONLY be used where you can validate the output is correct
at a glance.

Rewrite test driven development on a calculation with a non-obvious result,
for instance, is an antipattern.


## Where can I easily try it out for myself?

* [An interactive command line app with tests that rewrite themselves](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline)
* [A REST API with tests that rewrite themselves](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi)
* [A Python API with tests that rewrite themselves](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi)


## How do I do this?

* [HitchStory Rewritable Story Docs](../../using/engine/rewrite-story).
