{{{{ intro.txt }}}}

HitchStory is a python 
[testing and living documentation framework](approach/testing-and-living-documentation) for building strictly typed [executable specifications](approach/executable-specifications) which can [auto-generate your howto documentation](approach/triality).

The executable specifications can be written to specify, test and document applications at every level - replacing [xUnit](https://en.wikipedia.org/wiki/XUnit) equivalents of unit tests, integration tests and end to end tests with appropriate tooling.

The specifications are written using my other project [StrictYAML](why/strictyaml).

Fully fleshed out example projects (website, interactive command line, REST API and Python API) tested and documented with HitchStory executable specifications can be seen
[here in the examples project](https://github.com/hitchdev/examples/).

In these sample projects the website is tested with [playwright](https://playwright.dev/python/), the REST API tested using [requests](https://docs.python-requests.org/en/latest/index.html), the interactive command line with [icommandlib](https://github.com/crdoconnor/icommandlib) the python API tested with [hitchrunpy](https://hitchdev.com/hitchrunpy/).


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
