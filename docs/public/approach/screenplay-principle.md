---
title: Screenplay Principle
---

![Only what can be seen or heard](https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Screenplay_example.svg/593px-Screenplay_example.svg.png)

>The major components are action (sometimes called "screen direction") and dialogue. The action is written in the present tense and is limited to what can be heard or seen by the audience, for example descriptions of settings, character movements, or sound effects. The dialogue is the words the characters speak, and is written in a center column. -- https://en.wikipedia.org/wiki/Screenplay

The screenplay principle in software mirrors the #1 rule of visual writing - describe *behavior*,
step by step, in detail.

This is most commonly violated in two ways:

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

## Describing implementation rather than behavior

The other common antipattern which is not adhering to the screenplay pattern is to test implementation
rather than behavior, analagous to the screenplay writer who describes what the character thinks
rather than what the character does.

This is an instance of deliberately non-realistic testing. It can and does catch
bugs, but:

* It often triggers false positives (failures that aren't bugs) and doesn't catch actual bugs.
* It loses the ability to describe behavior in a way that is useful to stakeholders.
