---
title: What is the difference betweeen a test and a story?
---

While a test is turing complete code that tests behavior, a
story is turing-incomplete code which *defines* behavior.

A test is simply code that is executed and either raises
an exception indicating a failure or passes.

A story must be *played* using an execution engine.

A story can be translated into readable documentation, often with
the aid of artefacts created when running the story (e.g.
screenshots).
