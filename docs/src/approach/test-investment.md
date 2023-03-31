---
title: Tests as an investment
---

>1. You are NOT ALLOWED to write any production code unless it is to make a failing unit test pass.
>
>Now, most programmers when they first hear about this technique think "This is stupid!"
>"It's going to slow me down, it's a waste of effort, it will keep me from thinking, it
>will keep me from designing, it will just break my flow".
>
>- Uncle Bob, The Three Laws of TDD

I remember the first time I followed this rule to the letter - the tests were good, the code was clean and I ended up throwing it all away. I trialed the code in a real life situation and the code ultimately proved unnecessary.

The problem was it solved entirely the wrong problem - the customer didn't *want* the code I'd just TDD'ed.

TDD is a fantastically powerful approach which I always use by default, but there have been situations where it *hasn't* paid off because the cost of the tests was too high and the benefit was minimal in the end.

## The cost of building mocks

>Indeed, so long as we keep our tests short, well factored and well named, they ought
>to read very nicely. They ought to read like specifications; because they *are* specifications.
>
>- Uncle Bob, Test First

Like Bob, I believe that instead of tests you should indeed be writing specifications. *Unlike*
Bob, I don't believe turing complete code is an appropriate language for writing specifications
in. [Unit testing is wrong](../../why-not/unit-test).

If, instead of unit testing the hell out of everything, you subsribe to the notion that tests should
[closely mimic](../test-realism) your code's outside world, you must then start considering
how to build an approximation of the outside world.

This is not always easy. This is not always cheap. This does not always make sense. It *might*
be cheap if there is an easy to use [pre-existing project](https://www.selenium.dev/) that mimics
your code's outside world but there's no guarantee and if that project does not mimic reality
correctly then you may also be out of luck and you either have to improve that project yourself.

## The costs of false positives

Tests don't just fail in the presence of bugs. Tests can also fail in the presence of
changed code where no bug was introduced. This is a very common feature, in fact, of
tightly coupled tests.

When tests fail in the presence of a non-bug they incur a cost in the form of 

## The payoff of writing tests

There are four ways that automated tests can pay off:

* Catching bugs
* Giving confidence in the code
* Documenting the code
* Providing freedom to refactor
