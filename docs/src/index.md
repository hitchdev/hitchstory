{{{{ intro.txt }}}}

HitchStory is a python 3
[testing and living documentation framework](approach/testing-and-living-documentation) for building easily
maintained example driven [executable specifications](approach/executable-specifications) (sometimes dubbed
acceptance tests).

It was designed initially to make [realistic testing](approach/test-realism) of code less
of a chore so the tests would actually get written and run.

The executable specifications can be written to specify and test applications at
any level and have been used successfully to replace traditional
low level unit tests, integration tests and end to end tests
with easier to maintain tests.

The specifications are [written using StrictYAML](why/strictyaml) and the
code to execute them is written by you, in python.


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
