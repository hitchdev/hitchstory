---
title: Why unit testing needs to die
---

This is a controversial argument but, one that needs to be made:

  The world needs to move on from unit testing.

It ought to be noted that this is *not* an argument against any of the following,
which are often conflated with unit testing:

* Testing in general
* Property based testing (e.g. hypothesis).
* Test driven development
* The testing pyramid
* Mocking

All of those things are great. Please do not mistake this as an argument against
any of them in principle. None of them actually require the use of unit tests.

There are, broadly speaking, two applications of unit testing - one which works
okay and one of which works poorly enough that advocates for it are actually doing
great harm.

There are, broadly speaking, two types of code - algorithmic code and integration
code. Here are several examples of the former:

* A sorting algorithm (e.g. timsort or quicksort).
* Code in a business application that determines prices from a set of rules
* A function to slugify a title (e.g. The Silver Duck -> the-silver-duck).

Here are several examples of the latter:

* A basic CRUD application
* A device driver
* A simple javascript widget

Low level testing of algorithmic code
-------------------------------------

Low level testing of algorithmic code looks a little like this::

  def test_sort_five_items():
      assert sorted([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]

This is actually a good example of a clear test. The intent is obvious, the
label is descriptive. This is more or less how all tests should be.

This works because the code is, despite being turing complete,
declarative and simple.


High level testing of integration code
--------------------------------------



Rebuttals
---------

In the interests of openness and clarity and in recognition of 

Theoretically I'm interested in openness and clarity, so all of you who wish to offer
a rebuttal can open a pull request and link (rel="nofollow") to it here or raise a ticket.
