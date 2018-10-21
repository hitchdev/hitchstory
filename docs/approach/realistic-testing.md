---
title: The importance of test realism
---

Test realism is the strangely controversial principle that automated tests
should test code in as realistic a manner as possible.

This means, among other things:

- Running the code in an environment or environments that match where it will be run for real as closely as possible.
- Using and creating realistic mocks for the code to interact with that mimic the real thing as closely as possible.
- Prioritizing writing test scenarios that mimic the real life usage of the software.

While "test realistically" might *appear* to be incredibly obvious, it does, unfortunately,
conflict with certain more fashionable principles, chiefly
"[FIRST](https://pragprog.com/magazines/2012-01/unit-tests-are-first)".

Taken to extremes this means you get some people saying "[TDD test suites should run in
10 seconds or less](http://blog.ploeh.dk/2012/05/24/TDDtestsuitesshouldrunin10secondsorless/)"
which would mean, except for certain very specific kinds of software means you are
*guaranteed* to be writing and running *very* unrealistic tests.

FIRST stands for fast, isolated, repeatable, self validating and timely. It
was a set of principles developed by Tim Ottinger and Brett Schuchert for describing
ideal qualities of "unit tests" - the idea being that these would form the mainstay
of your automated test suite.

It does *not* stand for realistic. That quality - the quality which determines
how many bugs your tests actually catch is isn't even mentioned. I've no
doubt they consider it laudible - they apparently just don't consider it
*necessary*.


## The inherent trade off between test realism and test speed

While it's trite to say that a test that is fast and catches no bugs is pointless,
there's a little more to it than that.

Unrealistic unit tests *do* usefully catch bugs, which is partly why doing TDD
with them can be such a powerful approach. An unrealistic, quick test that
provides feedback on *some* bugs is still useful.

They just don't catch *as many* bugs, and they "catch" *far more* false positives.

Realistic tests, however, are usually slower than unrealistic tests.
It is possible (although rare) to make automated tests that are *incredibly*
realistic and unmanageably slow that don't actually catch significantly more
bugs than tests 1/100th of their speed.

There is, therefore, *always* a trade off to be made between incredibly
realistic and unmanageably slow and ultraquick but unrealistic.

It isn't necessarily a delicate trade off. There are quite frequently sharp
diminishing returns on both speed and realism.

If one test takes half a millisecond and another takes 500ms,
there isn't really *any* benefit to the quicker test - both are done in the
blink of an eye as far as the developer is concerned.

## Where do we draw the line?

Hypothetically speaking, lets say you have two tests testing the same feature -
one, a test which hits a real database and interacts with the real UI using
selenium. The other mocks out the UI (often dubbed "subcutaneous"
and the database).

One takes 25 seconds, the other takes 25 milliseconds - 1000x faster.

The unrealistic test gives *instantaneous* feedback if written in a test
driven style, while the realistic test can take up to 25 seconds to register
a failure.

However, the realistic test will catch a *lot* of bugs which the unrealistic
test will not and be less likely to fail when the feature works. In a relatively
straightforward web app an enormous proportion (if not most) of the bugs
you see will be "integration bugs" - bugs which emerge because of the interaction
between two modules or pieces of software - for example:

- The web page appearing the right way in one browser and the wrong way in another.
- The database returning the wrong result because it was called in the wrong way.
- The database performing an incorrect calculation because of how it was called.

*None* of these bugs will be caught with an unrealistic test that stubs or mocks
out the database - worse, you will likely also end up *embedding* bugs in the tests
which mock or stub the UI and the database and then having to undo them once
you test the actual app.

## Does this mean every test in every project should be an end to end test?

No, although for some projects, it's not necessarily a problem if they are.
Every project in hitchdev is tested that way. Even though they resemble unit tests
more than end to end tests, they do surround the entire project.

On the one hand, end to end tests that average < 25 seconds are an excellent
default approach. On the other hand, there are some tests that can be run
just as realistically and just as *easily* and be much faster and where that
is the case, it does indeed make sense to write faster tests at a lower level.

The *ideal* times to move testing to a lower level are when:

- There is a single module that has a clean abstraction and is loosely coupled to the module (or modules) around it.
- A different team is responsible for each module (this is where [executable specifications](../executable-specifications) also come in handy).
