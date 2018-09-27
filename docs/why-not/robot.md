---
title: Why not use the Robot Framework?
---

NOTE: This argument is a work in progress and there are still several things that need amending / adding.

HitchDev was, in a sense, inspired by the robot framework. I used it many years ago and became incredibly frustrated using it for debugging.

The last straw was trying to debug a robot test failure and discovering that the step that the test failed on was not displayed to the end user. It turned out that the maintainers had reasons for doing this, but they were bad reasons.

I eventually dumped it and used python's built in unit testing framework, which is unsuitable for many [other reasons](unit-testing-framework).

Robot did, I think, get one thing right - a feature it shares in common with cucumber and hitchstory - it enforced a clear separation of concerns between execution code and story definitions - a different kind of language to the one that executes the test.

However, it also made several mistakes:

# 1 The language is too complicated

The robot language was supposed to be a readable equivalent to python. Unfortunately, like many other languages that get on the DSL treadmill there were features added until it became Turing complete.

The language has conditionals, loops and variables - it essentially is a programming language, except not a very good one.


# 2 The debugging tooling is poor and the framework is not really designed to be ergonomic when debugging

TODO

# 3 RobotSelenium is tightly coupled to Robot

I made this mistake too initially when designing hitchstory. The temptation to have prewritten steps that could be plugged in (e.g. click) was pretty strong. It wasn't a good approach however - flexibility is too valuable.

In the end I figured that a better approach was to leave the contents of the step methods entirely up to the discretion of the developer and provide libraries that are framework agnostic. seleniumdirector may have been designed to work well with hitchstory and can be used to write some "one liner steps" like click but the API has no intrinsic connection to it and vice versa. It could work *just* as easily with py.test or unittest or be used to scrape websites.

Similarly all the libraries that form the hitch framework are designed to have a single, tightly scoped purpose (UNIX philosophy) and to be completely agnostic about what the programmer chooses to do with them.

