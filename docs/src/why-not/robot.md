---
title: Why not use the Robot Framework?
---

[HitchDev](https://github.com/hitchdev/hitchstory)'s creation was, in a sense,
inspired by the [robot framework](https://en.wikipedia.org/wiki/Robot_Framework).

I used it back in 2014 where it was deployed on a project I joined
and became *incredibly* frustrated using when debugging test failures.

Below I list the reasons that made me dislike this framework:

## 1. The debugging tooling is terrible

The last straw in 2014 was when I was trying to debug a test failure and 
discovered that the step that the line number and step the test failed on was not
displayed to me.

Yep, that's right, robot's reaction to a failing test wasn't "hey, there's a problem here"
it was "hey, something screwed up, why don't YOU figure out what?".

It turned out that the maintainers had [reasons](https://github.com/robotframework/robotframework/issues/549)
for doing this, but they were terrible.

I subsequently dumped it and used python's built in unit testing framework, which worked better
because it actually *told* me where it failed. It's still not a great framework
for many [other reasons](unit-testing-framework) but at least in that respect it was a breath
of fresh air compared to robot.

Hitchstory, of course, tells you exactly which line the code failed on and even gives
a stacktrace of the failed python code. I was very careful not to screw that up.

## 2. It doesn't fail fast

[Fail fast](../../../code-quality/fail-fast-fail-clearly) is a general principle of software development
whereby a system immediately reports at its interface any condition that is likely to indicate a failure.

Robot does not adhere to this principle.

One example of how it breaks this principle is what happens if you put in an unknown keyword. It will
run the 

## 2. The DSL is turing complete

There is a common pattern among DSLs that I call the "DSL treadmill". Somebody identifies a problem
and thinks "I know, I'll create a DSL to solve this problem". That DSL works for a while and the creator
soon some use cases which they think it would be good to accomodate. Then they add some features.
Then they see some other use cases. Then they add some more features.

Then, at some point, *whoops* they've created a turing complete programming language... by *accident*.
This has happened to, among other DSLs [C++ templates, server side includes, mediawiki templates and
sendmail configuration files](http://beza1e1.tuxen.de/articles/accidentally_turing_complete.html) all
of which are notoriously hellish to use.

While more features sounds like a good thing at first glance, with turing completeness being a
quirky side effect of interest only to the academically inclined, it's actually a horrible, *horrible*
trap to accidentally create a programming language.

Turing complete code is, by its nature, difficult to understand. It requires years of practice to
read and get what is going on. Even *after* those years of practice, correctly ascertaining behavior
from a turing complete program is often infeasibly difficult which is... well, why we need to test
software.

The features robot added which tipped it over the edge were conditionals, loops and variables.

At that point, what was even the point of *having* a DSL? Python is a *much* better programming
language. If you're going to write turing complete tests, you should at least write it in that.

Moreover, high level tests shouldn't describe behavior with conditionals and loops, they should
describe *behavior* as a declarative sequence of actions.


## 3 RobotSelenium is tightly coupled to Robot

I made this mistake too initially when designing hitchstory. The temptation to have prewritten steps that could be plugged in (e.g. click) was pretty strong. It wasn't a good approach however - flexibility is too valuable.

In the end I figured that a better approach was to leave the contents of the step methods entirely up to the discretion of the developer and provide libraries that are framework agnostic. seleniumdirector may have been designed to work well with hitchstory and can be used to write some "one liner steps" like click but the API has no intrinsic connection to it and vice versa. It could work *just* as easily with py.test or unittest or be used to scrape websites.

Similarly all the libraries that form the hitch framework are designed to have a single, tightly scoped purpose (UNIX philosophy) and to be completely agnostic about what the programmer chooses to do with them.


## What did Robot get right?

Robot did, I think, get one thing right - a feature it shares in common with [gherkin/cucumber](../gherkin) and [hitchstory](../../) - it enforced a clear separation of concerns between execution code and story definitions - a different kind of language to the one that executes the test. It was this core of a good idea that inspired me to write my own framework.
