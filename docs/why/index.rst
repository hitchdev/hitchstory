---
title: HitchStory Philosophy
---

HitchStory is a BDD/ATDD framework for writing executable stories which follows a set of 10 principles.

These principles both differ slightly from BDD principles and go beyond them.


Story Principles
----------------

#1 Stories should follow the "screenplay principle" - if it is visible to the user, it should be reflected in the story.

Note that this differs from the principle of BDD that "if it is interesting to the business" it should be reflected in the story.

#2 Stories should be *specified* in a non-turing complete configuration language with preconditions, steps, parameters and metadata.

Turing completeness is both a blessing and a curse. According to the rule of least power, the language you use for any given task should
be as powerful as required but *no more powerful*.

A symptom of languages that are too powerful is an excess of technical debt, a lack of readability and maintainability.

Languages that are not powerful enough will prevent the user doing the task at hand, often necessitating nasty hacks to circumvent the lack of power.

Specifications should not require turing completeness.

#3 Stories should be written by programmers, be understandable by expert users of the software and generate documentation for non-expert users of the software.

Written by programmers:

While it is not strictly necessary for programmers to write stories, there are a number of non-obvious pitfalls
which non-programmers (and even beginner programmers) can and will fall in to when writing stories:

* Specifying implementation details rather than defining behavior.
* Writing repetitive stories.
* Missing key edge cases.
* Being too specific or not specifc enough.
* Not seeing or understanding where stories need refactoring.

Note that this contrasts with some interpretations of BDD, where product owners are supposed (in theory) to write stories which will be implemented by developers.

Understandable by expert users of the software

HitchStory stories are *not* English and not intended to be English, however they are designed to be simple and structured in an obvious way
while maintaining syntactic terseness as well as being DRY.

Expert users who are familiar with the domain and the software should be able to understand the stories,
picking up on contextual clues where necessary without the need for additional training to understand the language.

Because stories are written to be DRY, they will often lack contextual information and be devoid of explanations of the software domain,
so it does not work ideally as a form of documentation for use by everybody.

Generate documentation for non-expert users of the software

Non-expert users will need documentation describing the system's behavior too, although they will need a lot more context in order to
understand what is going on.

Using the stories and their metadata as a base, it should be possible to generate highly readable, well written documentation
that even a beginner being introduced to the software should be able to understand.

Readable, highly contextual documentation will not be DRY.



#4 Small changes in the software should automatically rewrite stories where appropriate.

#5 Stories should be made DRY using inheritance and parameterization.



Engine Principles
-----------------

#1 The engine code, written in a turing complete language, should *only* execute and verify stories and generate documentation.

#3 While story defintions should be written in a declarative, non-turing complete language, the story engine that executes, verifies the stories and generates the documentation - the story *engine* needs to be written in a turing complete language to allow the flexibility.

#3 Mocks should be as realistic as is feasible given resources and time to run and build.

#4 Where the real thing is cheap and fast enough to use, use the real thing (e.g. a database) instead of using a mock or a less realistic equivalent (e.g. sqlite instead of postgres).

#5 Where the real thing would be expensive to invoke regularly (e.g. a story that sends an SMS via a REST API), use tools to generate a mock equivalent from the real thing.
