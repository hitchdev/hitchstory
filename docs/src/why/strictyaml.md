---
title: Why does HitchStory use StrictYAML?
---

YAML is [routinely criticized](https://noyaml.com) and **rightly so**.

HitchStory storytests are written using StrictYAML for three reasons:

* It enforces a separation of concerns between your declarative specification and imperative testing code.
* The storytests can be programmed to *rewrite themselves* from program output which makes [snapshot test driven development](../../approach/snapshot-test-driven-development-stdd/) easy.
* The storytests can be used as a template to generate beautiful markdown documentation - which makes documentation driven development easy.

**None of these features are worthwhile**, however, if the storytests are interpreted using a normal YAML parser.

When I first built hitchstory I ran face first into ALL these problems when I tried to build it with pyyaml - strings randomly turning into numbers, confusing errors caused by mis-indentation. My job experienced what I later dubbed [the Norway problem](/strictyaml/why/implicit-typing-removed/). I felt the YAML hate.

However, I still liked how YAML looked. The core of YAML is still a very clean, beautiful format to look at. It just had some *horrible* unnecessary features and was in dire need of type-safety.

This is why I built [StrictYAML](/strictyaml). Although I built it so I could build hitchstory, it became popular on its own.

With hitchstory I could write specifications that:

* Are 100% declarative.
* Display complex hierarchical data cleanly (e.g. adding required request headers to a REST API story would be easy).
* Have minimal syntactic noise.
* Display multi-line strings cleanly.
* Look familiar to most people.
* Can be used with existing syntax highlighters.

All of this was pointless though, if it wasn't safe to edit because a single quotation mark or a mis-indent leads to 20 minutes of debugging. So, the existence of StrictYAML became a necessary prerequisite for hitchstory.

With HitchStory, the core structure of user stories is fixed, but metadata, preconditions and steps require user defined mini-schemas for anything more complex than a string. Here is an example that validates a step that interprets a REST API request and response: https://github.com/hitchdev/hitchstory/blob/master/examples/restapi/tests/test_integration.py#L35 (see everything in @validate).

## Avoiding building a YAML programming language

Ansible was an inspiration for hitchstory because the first time I saw it I could see how clean, easy to use and readable the YAML runbooks were.

However, I also saw what happened when those runbooks became complicated.

Ansible fell into what I call the "turing completeness trap" - configuration languages that start out fine and then, after trying to solve a particular problem, accidentally become turing complete. The typical features which cause this are conditionals and loops.

These YAML languages aren't good programming languages though, and that becomes particularly noticeable when you try to debug them.

A few continuous integration YAML tools also fall into the turing completeness trap and debugging them can also be painful.

HitchStory will **never** implement conditionals or loops in the specification language. *Test engines* that interpret the specifications will requires conditionals and loops, but specifications never, ever will.
