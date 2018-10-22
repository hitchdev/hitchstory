---
title: Screenplay Principle
---

>All of the writing in a screenplay must create an experience similar to that of watching a film. So, while in a novel you may be able to say:

>>Jessica sits on a bench and thinks of John. She misses him deeply. She thinks about the birthday parties, the Valentine’s Day dinners, the walks on the beach. She cries for the love they shared and the love they’ve lost.

>In a screenplay, if you imagine the scene visually, all you’re really experiencing is:

>>Jessica sits on a bench, staring down at her feet. After a moment she begins to cry.

>-- [Lauren McGrail, Lights Film School](https://www.lightsfilmschool.com/blog/what-visual-storytelling-looks-like-in-a-screenplay-aes)

The screenplay principle in software mirrors the #1 rule of visual writing - describe and test behavior,
*not* implementation.

Before declaring how the screenplay principle *should* be followed, I will first describe a few
common anti-patterns where it isn't:

## Describing implementation details

The most common and egregious way this principle is violated is with low level unit tests exhibiting a high level of mocking. Unit tests can only describe the behavior of classes and methods - something that is generally only of interest when your users are other developers (i.e. you're writing a library).

## Describing in too little detail how a program behaves

Another common violation of this principle is to write tests or specs that are
too vague. This is argued as a good practice in the blog post
[the training wheels come off](http://aslakhellesoy.com/post/11055981222/the-training-wheels-came-off)
by Aslak Hellesøy, the creator of Cucumber, wherein he declares "screenplay scenarios"
like the following to be brittle:

```gherkin
Scenario: Successful login
  Given a user "Aslak" with password "xyz"
  And I am on the login page
  And I fill in "User name" with "Aslak"
  And I fill in "Password" with "xyz"
  When I press "Log in"
  Then I should see "Welcome, Aslak"
```

>The idea with Cucumber (and BDD in general) is that stakeholders assist in writing scenarios - or executable specifications. This solves the where do we start problem with TDD. The scenarios express what a user should be able to do, and not how. When a scenario is defined, programmers implement the required functionality.
>
>This kind of workflow is much harder to follow when scenarios are written in a low-level, imperative style. Very few stakeholders or business analysts are going to agree to defining functionality in terms of mouse clicks and key presses. They think and talk at a higher abstraction level, and scenarios should capture that.

This isn't completely wrong. It *is* typical that stakeholders and business analysts will
define functionality in terms of mouse clicks and key presses. However:

- Just because a business analyst won't typically be the one defining functionality and behavior in terms of mouse clicks and key presses it doesn't mean that they never care about that level of detail.
- A business analyst won't define in that level of detail, but a UX/UI analyst working in concert with them may well define in this level of detail.
- "What a business analyst defines" is generally *not* a good basis for an executable specification, although it might make a good basis for a user story title.

Cucumber stories still aren't a good vehicle for the screenplay pattern since they do not allow inheritance, [unlike hitchstory](../../why/inheritance).
