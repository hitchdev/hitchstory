---
title: Testing non-deterministic code
---

Non-deterministic code is an inevitable fact of life, but it's a monumental pain
to test.

Non-deterministic code is code which can produce different outputs even
when it is given the same inputs. For example: a program that is asked to output
the three most popular fruits might list *"apple, banana and orange"* but it could
give *any* arbitrary order for those fruits - for example *"orange, banana and apple"*.

Often the end user or customer won't actually care about non-determinism - the ordering
of the fruit might not matter.

However, your automated tests *will* care - if you write a test that expects
"apple, banana and orange" then you will get a [flaky test](../flaky-tests) that
will pass and fail arbitrarily.

There are five approaches I usually take to dealing with testing non-deterministic
code with [hitchstory](https://github.com/hitchdev/hitchstory) which I listed
here in preference order.

If you're currently facing a non-determinism problem, you can treat this as a kind
of guideline or tutorial when facing a non-determinism issue:

## 1. Make the code deterministic

With the sole exception of code where randomness is a desired property, more deterministic
code is *better* code. It's a code quality like DRY or loose coupling, which is a
laudable goal.

More deterministic does not just mean easier to test, it means a restricted execution
space. In practical terms, a restricted execution space means fewer potential avenues
for surprise bugs to crop up - the kind of bugs which yield a 4am phone call from a
customer and when you try it yourself on your laptop *you don't get the bug*.

While a small amount of determinism isn't necessarily a problem for the customers,
it can quickly spiral out of control when non-deterministic behavior is compounded
with other non-deterministic behavior. If non-deterministic behavior is *multiplied*
and when that happens the number of potential edge cases where bugs can be harbored
can spiral out of control.

However, indeterminism crops up in all sorts of places naturally in code,
which are not that hard to eliminate. Here are two common ones, which I would
usually treat as bugs *even if* the customer has told you they don't care:

### SQL SELECT statements without an ORDER BY

Select statements without an order by usually output in the same order each time but
they won't always. You could write a perfectly good functioning test on your laptop
that expects a certain order from the select statement (e.g. it checks the first
product on the page) and then that test can fail randomly the next day or on the
continuous integration machine because it has moved.

This one has happened to me *a lot*. It's happened so many times that if I see
a pull request with a SELECT (or ORM equivalent) without an order by I will
always treat it as an issue that needs to be fixed even if it is unlikely to
cause an issue.

Where not having an order by is the cause of a flaky test, this is generally the
best fix.

### Non-ordered dictionaries / hashmaps

In python one of the most common data structures used is the 'dictionary' - this
is an association of "keys" to "values" - e.g.

```python
my_dictionary = {
    "fruit": "apple",
    "car": "ford",
    "coffee": "arabica",
}
```

If all the code does is look up one from the other then there will never be a problem.
However, if the code tries to *cycle* through all of these things *then* there is a
problem. For example:


```python
for kind_of_thing, thing in my_dictionary.items():
    print(kind_of_thing)
```

The problem here is that there is often no guaranteed order to the things in the dict.
It's given as "fruit", "car", "coffee" but you might get "coffee", "car", "fruit" -
and you probably *will*, eventually.

You can guarantee the ordering in python by using "OrderedDict" (which will always
remember the ordering) or by using any version of python above 3.6.

While this is a notable problem in python, many other languages suffer from the same
issue. It can (and frequently) does crop up in *libraries* that you rely upon.

### Sometimes you can't fix this though

While these fixes are likely quick and easy for some code, especially if you work
with helpful developers (or you *are* the developer), it's not always so easy to fix.
For example:

* You might be using a library that is non-deterministic and fixing it simply isn't feasible.
* The developers you work with might be intransigent and unwilling to expend time to help.
* You might be working with some kind of inherently non-deterministic code (e.g machine learning code).
* It might be possible to fix but simply an *enormous* amount of work that you don't have time for.
* Random numbers might be a critical feature of the application.

If the indeterminism is unfixable, then move on to...

## 2. Isolate the non-determinism and test the code that relies upon it separately

Let's say that you're testing some kind of strategy game that uses a virtual dice roll.
It is virtually impossible to end to end test this game normally by using deterministic
means because the outcome each time will be different.

You can, instead, write the code such that the "dice roll" is always gotten from the
same function. You can then make that function usable in "test" mode and "real"
mode and in test mode, it can get the numbers deterministically from a file which your
test can prepopulate.

Voila, you have now isolated the non-determinism and you now have an easily testable
game where you can verify consistently what happens when different dice rolls are thrown.

Sometimes, of course, *you can't easily do this* - maybe the code change would be difficult
(e.g. random numbers are called in a different way all over the code base) or, once again,
you're dealing with an intransigent developer. Where this isn't possible, another possible
approach is output transformation:

## 3. Output transformation

Let's say that instead of a strategy game that uses a virtual dice roll you are simply
testing virtual six sided dice - nothing fancy, just a command line application that
outputs:

```
You rolled a 6!
```

The output here is always going to be of the form "You rolled an n!". Since this
structure is guaranteed, you can write test code that takes the output
and transforms "You rolled a 1!" *or* "You rolled a 2!" and turns it into
"You rolled an n!".

You can do this transformation with  a regex or a templex and then the
specification can check the transformed version is "You rolled an n!".

The downside to this approach is that it requires test code that is often rather
complicated and can have bugs *itself*. The upside is, of course, that it works
even if you don't have access to the application code and cannot change it easily.

## 4. List multiple valid outputs in your test

I once worked on an application where there was a web page that listed two
products on a web page - the cheaper version and the expensive version. I
was attempting screenshot testing and I realized that sometimes the cheaper
version would appear on the left and sometimes it would appear on the right.

I got two completely different screenshots. I notified the stakeholders and they
were indifferent. The code itself could have been changed to stop doing this
but, for various reasons, it would have been hard and risky to do this.

Instead of doing that, I simply created two screenshots for each version and
verified that *at least one* of them was displayed. It wasn't necessarily the
nicest solution, but it was cheap and it worked.

## 5. Test a property of the output rather than the output itself

Some of the more eagle eyed of you might have realized that the test that
tested the die roll above missed a very critical detail: if the die rolled
a seven or worse, a zero the test would still have passed but it would have
passed in the presence of a bug.

This isn't necessarily the worst thing ever - writing an automated test
for every last thing is an expensive [test investment and sometimes
test investments don't pay off](../test-investment).

However, if you are committed to doing this, the test above can be extended
not just to transform the output from "You rolled a 6!" to "You rolled an n!",
it can be transformed and the number can be extracted. This number can then
be *property tested*. There are various things you could do to property test
it and it may pay to do them in more or less detail. In this case, for example,
you could test any of the following:

* The number is negative.
* The number is an integer.
* The number is above 0 but below 7.

## Conclusion

Use whichever method makes the most sense, but show a bias towards changing
the *code* to be deterministic rather than the tests.
