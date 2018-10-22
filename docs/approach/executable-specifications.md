---
title: Executable specifications
---

An executable specification is an idea taken from
[agile philosophy](http://www.agilemodeling.com/essays/executableSpecifications.htm):

>When trying to understand a class or operation most programmers will first look for sample code that already invokes it. Well-written unit/developers tests do exactly this – they provide a working specification of your functional code – and as a result unit tests effectively become a significant portion of your technical documentation. Similarly, acceptance tests can form an important part of your requirements documentation. This makes a lot of sense when you stop and think about it. Your acceptance tests define exactly what your stakeholders expect of your system, therefore they specify your critical requirements.

It differs from a normal test primarily because it doubles as a means of clearly *describing*
the software behavior *as well as* something you can feed to a machine that will
test your code.

The three preconditions for this are:

* A clear separation of concerns between specification and execution code
* A clear segregation barrier between the environment that *executes* your tests and the environment *under* test.
* The executable specifications are described using declarative markup instead of turing complete code
