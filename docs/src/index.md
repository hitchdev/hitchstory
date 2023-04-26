{{{{ intro.txt }}}}

HitchStory is a literate python testing framework where the tests can rewrite themselves and [write your docs](approach/triality).

[![Test rewriting itself](https://hitchdev.com/images/video-thumb.png)](http://www.youtube.com/watch?v=Aqk5Sao27O0 "Test rewriting itself")

The executable specifications are written, using [StrictYAML](why/strictyaml) and
can test and document applications of any kind.

Fully fleshed out examples (a website, an interactive CLI, a REST API and Python API) with self rewriting tests and generated docs can be seen
[in the examples folder](https://github.com/hitchdev/hitchstory/tree/master/examples)
and run.

The library is 100% pure python. The tests can be run:

* [Inside pytest or similar](https://hitchdev.com/hitchstory/using/pytest)
* [Or via a basic CLI runner](using/basic-cli)


## Example

{{{{ quickstart.txt }}}}


## Install

```bash
$ pip install hitchstory
```

## Using HitchStory

{{{{ using-contents.txt }}}}

## Approach to using HitchStory

Best practices, how the tool was meant to be used, etc.

{{{{ approach-contents.txt }}}}

## Design decisions and principles

Design decisions are justified here:

{{{{ why-contents.txt }}}}

## Why not X instead?

There are several tools you can use instead, this is why you should use this one instead:

{{{{ why-not-contents.txt }}}}
