---
title: Complementary tools
---

hitchstory is designed to be used with python tools
to interact with your app. There are a number of excellent
libraries which have been tested with and work quite well
with hitchstory.

Inside the examples given, you can see the libraries being
used in a file called `engine.py` in the `hitch` folder.


## [Playwright](https://playwright.dev/python/docs/intro)

Example Project: https://github.com/hitchdev/hitchstory/tree/master/examples/website

If you are testing a website, this is a good go to library.
Little more needs to be said about it.

The example project also makes use of playwright's video and
screenshot generation to generate documentation that is more alive.

While perhaps not ideal from a BDD the selectors can be specified
in a YAML story.

## [Requests](https://requests.readthedocs.io/en/latest/)

Example project: https://github.com/hitchdev/hitchstory/tree/master/examples/restapi

Requests is one of the most famous python libraries. It is probably the simplest
and easiest way to call REST APIs and get a response.

The example project demonstrates how the response from requests
can be used to rewrite the stories.


## [ICommandLib](https://hitchdev.com/icommandlib)

Example project: https://github.com/hitchdev/hitchstory/tree/master/examples/commandline

This library was written for use with hitchstory so that interactive
command line applications could be tested.


## [hitchrunpy](https://hitchdev.com/hitchrunpy)

Example project: https://github.com/hitchdev/hitchstory/tree/master/examples/pythonapi

This library was written for use with hitchstory. It runs snippets
of python code against a specified python interpreter.

This library is a product of dogfooding. Every library published
on this website is tested with hitchrunpy and hitchstory, and all
"howto" documentation is generated using stories which are tested via
hitchrunpy.

If you want to build, test and document a Python API with hitchstory,
this is the library to use.

