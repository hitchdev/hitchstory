---
title: Why use hitchstory instead of a unit testing framework?
---

This is *not* an argument against the following:

* Testing in general
* Test driven development
* Low level testing (of classes and methods or otherwise)
* Property based testing (e.g. hypothesis).
* Mocking
* Doctests

All have their place.

This simply about the use of unit testing frameworks - py.test, nose, unittest2, jUnit, etc.
for low level testing, integration testing *and* end to end testing.

There are, broadly speaking, two types of code - algorithmic code and integration
code. Here are several examples of the former:

* A sorting algorithm (e.g. timsort or quicksort).
* Code in a business application that determines prices from a set of rules
* A function to slugify a title (e.g. The Silver Duck -> the-silver-duck).

Here are several examples of the latter:

* A basic CRUD application
* A device driver
* A simple javascript widget

## Low level testing of algorithmic code

Low level testing of algorithmic code looks a little like this example testing an 'incrementor' from the py.test home page:

```python
def test_answer():
    assert inc(3) == 4
```

This is actually a good example of a clear test. The intent is obvious, the
label is descriptive.

This works because the code is, despite being turing complete,
declarative and simple.


## High level testing of integration code

Ultimately it boils down to two programming principles which hitchstory provides 'rails' to guide
you:

* The rule of least power
* Separation of concerns

Hitchstory stories describe a sequence of events which describe either a user or a user-system
interacting with your code. This can be used to describe the functioning of any software system.
It is not necessary** to use turing complete code to describe a sequence of events, therefore,
according to the rule of least power, you shouldn't use turing complete code to do it.

However, turing complete code *is* required to set up and mimic this set of events. This is
what the hitchstory engine is used for, which must be written in turing complete python.

This divide between story definition and story execution also creates a natural barrier for the
separation of concerns. Story definition goes in the stories while execution goes in the engine.
Unit testing frameworks do not have any such natural barrier for separation of concerns.

Web developers may be familiar with this principle as it is expressed in web development
frameworks where (intentionally less powerful) templating languages are used to render HTML,
separated by a divide from more powerful 'controller' (or, in Django, 'view') code.

Other features which are not (and cannot) be duplicated in unit testing frameworks:

## Automated story modification

The hitchdev framework does come with a lot of useful testing tools which could just as
easily be used with py.test if you so wish.



## Rebuttals

