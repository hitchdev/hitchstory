---
title: Why not use Cucumber or other Gherkin-derived languages?
---

Python equivalents: lettuce, behave
Java equivalent: JBehave

Cucumber was the original 'BDD' frameworks and probably the most popular. It is essentially
a parser for the Gherkin language, which is a high level "English-like" declarative language
that can be used to specify user stories which can be executed.

This approach has the following advantages:

* Stories are descriptive and declarative. Turing complete languages (python, Java, Ruby, C, etc.) are more powerful than necessary to describe user stories. Using a separate, less powerful language to describe them aids readability and maintainability.

* A language barrier can help maintain separation of concerns between story definition code and story execution code.

HitchStory aims to maintain these benefits while improving upon the language

Avoiding ambiguous parsing: abandonging English-like sentences
--------------------------------------------------------------

   Some people, when confronted with a problem, think "I know, I'll use regular expressions." Now they have two problems. - Jamie Zawinksi

English is an ambiguous language. While this has 
The use of regular expressions in cucumber was done as a hack to enable the use of
"English-like" sentences in the construction of user stories.

There are a multiplicity of examples around the web where it went wrong causing headaches
for users.

http://coryschires.com/ten-tips-for-writing-better-cucumber-steps/


Strong typing
-------------




Verbosity
---------

The stories are much longer than they need to be.


A lack of inheritance
---------------------

