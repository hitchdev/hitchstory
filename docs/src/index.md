{{{{ intro.txt }}}}

HitchStory is a [StrictYAML](why/strictyaml) based integration testing library
that runs in pytest. With it you can build:

## Integration tests which generate their own documentation

![Test writing docs](https://hitchdev-videos.netlify.app/rewrite-docs-demo.gif)

## Integration tests that rewrite themselves

![Test rewriting itself](https://hitchdev-videos.netlify.app/rewrite-demo.gif)

## Example projects:

* [A website (with playwright)](https://github.com/hitchdev/hitchstory/tree/master/examples/website)
* [An interactive command line app](https://github.com/hitchdev/hitchstory/tree/master/examples/commandline)
* [A REST API](https://github.com/hitchdev/hitchstory/tree/master/examples/restapi)
* [A Python API](https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi)


{{{{ quickstart.txt }}}}


## Install

```bash
$ pip install hitchstory
```

## Using HitchStory

Every feature of this library is documented and listed below:


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

## Using HitchStory: Setup on its own

If you want to use HitchStory without pytest:

{{{{ using-setup-contents.txt }}}}

## Using HitchStory: Behavior

Miscellaneous docs about behavior of the framework:

{{{{ using-behavior-contents.txt }}}}
