{{{{ intro.txt }}}}

HitchStory is a [StrictYAML](why/strictyaml) based python integration testing framework where the tests can [rewrite themselves](why/rewrite) and [write your docs](approach/triality).

[![Test rewriting itself](https://hitchdev.com/images/video-thumb.png)](https://vimeo.com/822561823 "Test rewriting itself")

It can be used to quickly and easily integration test and generate docs for any kind of app. Examples:

* [A website](https://github.com/hitchdev/hitchstory/tree/master/examples/website)
* [An interactive command line app](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline)
* [A REST API](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi)
* [A Python API](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi)


## Example

{{{{ quickstart.txt }}}}


## Install

```bash
$ pip install hitchstory
```

## Using HitchStory: Setup

Skeleton set up with example stories:

{{{{ using-setup-contents.txt }}}}

## Using HitchStory: With Pytest

If you already have pytest set up and running integration
tests, you can use it with hitchstory:

{{{{ using-pytest-contents.txt }}}}

## Using HitchStory: Engine

How to use the different features of the story engine:

{{{{ using-engine-contents.txt }}}}

## Using HitchStory: Documentation Generation

How to autogenerate documentation from your tests:

{{{{ using-documentation-contents.txt }}}}

## Using HitchStory: Inheritance

Inheriting stories from each other:

{{{{ using-inheritance-contents.txt }}}}

## Using HitchStory: Runner

Running the stories in different ways:

{{{{ using-runner-contents.txt }}}}

## Approach to using HitchStory

Best practices, how the tool was meant to be used, etc.

{{{{ approach-contents.txt }}}}

## Design decisions and principles

Design decisions are justified here:

{{{{ why-contents.txt }}}}

## Why not X instead?

HitchStory is not the only integration testing framework.
This is how it compares with the others:

{{{{ why-not-contents.txt }}}}

## Using HitchStory: Behavior

Miscellaneous docs about behavior of the framework:

{{{{ using-behavior-contents.txt }}}}
