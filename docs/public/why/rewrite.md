---
title: Why Rewritable Test Driven Development (RTDD)?
---

Rewritable test driven development is a form of test driven development
where the developer changes some code, runs a test in rewrite mode
and the test runner *rewrites* the test to match the changed output.

Example:

[![Test rewriting itself](https://hitchdev.com/images/video-thumb.png)](https://vimeo.com/822561823 "Test rewriting itself")

In the above example:

1. The test is run with the old text - "To-do list" and PASSES.
2. The code is tweaked to say "My to-do list" instead.
3. The test is run in normal mode and FAILS.
4. The test is run in rewrite mode and PASSES, rewriting the test.
5. The test is changed and PASSES when run in normal mode.

The video also demonstrates how to adjust the engine to make the test rewrite.

## Why do this?

You can save a LOT of time with this technique. It makes integration test driven
development worthwhile.

Traditional test driven development implores you to always
[construct a test first and write the code that makes it pass after](https://en.wikipedia.org/wiki/Test-driven_development#Test-driven_development_cycle).

Where a desired output is trivial to validate at a glance but tedious
to construct, this is a waste of time.

It is far better to write the code to generate the output, let the
testing framework rewrite the test and manually check the rewritten
test before committing them both.

This technique is particularly useful for integration tests that validate
things like:

* The output of command line applications (as demonstrated above).
* Exact error messages with context displayed on a website.
* REST API responses.


## When *not* to use it?

This technique must ONLY be used where you can easily validate the output is correct
at a glance.

Rewrite test driven development on a calculation with a non-obvious result,
for instance, is an evil antipattern.


## Where can I see this in action?

If you check out the [hitchstory repo](https://github.com/hitchdev/hitchstory), you can try this out yourself on the three example "to do" app projects with integration tests:

* [An interactive command line app with tests that rewrite themselves](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline)
* [A REST API with tests that rewrite themselves](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi)
* [A Python API with tests that rewrite themselves](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi)


## Where are the docs?

* [HitchStory Rewritable Story Docs](../../using/engine/rewrite-story).
