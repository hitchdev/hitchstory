---
title: Why does HitchStory use StrictYAML?
---

HitchStory stories are written using YAML because it:

* Has a clear and obvious layout and relationships driven by its indentation structure.
* Has minimal syntactic noise.
* Displays complex hierarchical data cleanly.
* Displays multiline strings cleanly.

These features make it a particularly good fit for writing declarative stories with, since
they often require a lot of hierarchical data and multiline strings to display clearly.

Its relative existing popularity also means that it is somewhat familiar to a lot of people
and there is a lot of existing tooling which can be used (e.g. syntax highlighters in text editors).

## Why StrictYAML though?

YAML unfortunately contains additional quirks which cause havoc in other applications.

[StrictYAML](../../../strictyaml) is a YAML parser with that parses a restricted subset of YAML. The
subset rejects most of YAML's horrible quirks like that horrible Norway thing.

The parser also contains a means for creating schemas which can be used to validate YAML 
document structures and quickly reject invalid documents.

This schema language is integrated with hitchstory and can be used to validate the YAML structure of
preconditions, additional metadata and step arguments.
