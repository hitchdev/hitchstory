---
title: Why does hitchstory mandate the use of given but not when and then?
---

[Given-When-Then](https://en.wikipedia.org/wiki/Given-When-Then) is a structured
way of writing test cases or executable specs. It was invented by Dan North as
part of behavior driven development.

## Hoare logic

This pattern is a structure that essentially all test cases should be written,
separating the preconditions from the actions from the observable outcome. It
follows from [Hoare logic](https://en.wikipedia.org/wiki/Given-When-Then)
- a means of reasoning rigorously about the correctness of a computer program.

Many BDD frameworks have *explicit* keywords for given, when and then. These
keywords are intended to describe the structure of the story in a 'readable'
way.

## But what does given, when and then actually do?

Crucially, though, keywords *don't actually do anything*. In Cucumber, for example,
there is no meaningful difference to putting "when" and "then" - they are
essentially null operators.

I view them as something akin to test case writing "training wheels" - they are
useful for beginner testers to keep the tester/specifier on track, ensuring
that the test cases created are meaningful and actually test.

However, while training wheels are useful for beginners, they become cumbersome
and get in the way once you no longer need them.

## Terseness and clarity

Hitchstory recognizes that the pattern describes the structure of how *should* be
written but, other than given, it neither requires nor encourages that the
actual keywords be used.

Terseness is a key principle of hitchstory - the idea that stories should be
as short and non-repetitive as possible, provided it doesn't inhibit readability.

As an example, in this case, "click" is the "when" step and "goes kaboom" is the
then step. The story is still clear without them:

```yaml
given:
  box: red
steps:
- click: red button
- goes kaboom
```

## Still optional

Nonetheless, if you choose, you can create steps that start with when and then:

```yaml
Given:
  I have: red box
Steps:
- When I click: the red button
- Then it goes kaboom
```
