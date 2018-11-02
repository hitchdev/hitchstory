---
title: Screenplay Principle
---

>All of the writing in a screenplay must create an experience similar to that of watching a film. So, while in a novel you may be able to say:

>>Jessica sits on a bench and thinks of John. She misses him deeply. She thinks about the birthday parties, the Valentine’s Day dinners, the walks on the beach. She cries for the love they shared and the love they’ve lost.

>In a screenplay, if you imagine the scene visually, all you’re really experiencing is:

>>Jessica sits on a bench, staring down at her feet. After a moment she begins to cry.

>-- [Lauren McGrail, Lights Film School](https://www.lightsfilmschool.com/blog/what-visual-storytelling-looks-like-in-a-screenplay-aes)

The screenplay principle in software mirrors the #1 rule of visual writing - describe *behavior*,
step by step, in detail.

There are two main ways to violate this principle

## Skimping on user focused details

In [the training wheels come off](http://aslakhellesoy.com/post/11055981222/the-training-wheels-came-off)
by Aslak Hellesøy, he argues, I think wrongly, for writing specifications that look like this:

```gherkin
Scenario: User is greeted upon login
  Given the user "Aslak" has an account
  When he logs in
  Then he should see "Welcome, Aslak"
```

This narrative leaves out a lot of potentially relevant details. It is unclear what "Aslak" is - is it
a username? is it a user's name? It's also unclear *how* the user logged in - did it happen via SSO?
Perhaps it happened with a web page?

Missing out these details hurts from many different angles:

* The stakeholder defining behavior might forget potentially important edge cases when going through the scenarios because they don't see the subtle, relevant trigger ("maybe if SSO happens because the user is already "logged in" then welcoming them makes no sense...?"). 

* Stakeholders who are interested in the finer details of the software's behavior (e.g. security analysts), it's not useful as a means of communication.

* It will likely lead to the implementer forgetting to document, implement and test important edge cases.

* It will frequently not be detailed enough to describe the steps needed to reproduce a bug in precise enough detail.

## Testing implementation rather than behavior

The other common antipattern which is not adhering to the screenplay pattern is to test implementation
rather than behavior, analagous to the screenplay writer who describes what the character thinks
rather than what the character does.

This is an instance of deliberately non-realistic testing. It can and does catch
bugs, but:

* It often triggers false positives (failures that aren't bugs) and doesn't catch actual bugs.
* It loses the ability to describe behavior in a way that is useful to stakeholders.
