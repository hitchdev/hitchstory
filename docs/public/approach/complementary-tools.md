---
title: Recommended complementary tools
---

This library was also designed alongside a number of other recommended tools which seamlessly
integrate with hitchstory, providing functionality to easily build and to test various different
kinds of software.

* [hitchkey](https://github.com/hitchdev/hitchkey) - create a project "key.py" of simple methods that can be used to run project-specific commands written in python 3 in an isolated virtualenv and easily run them directly from the command line (e.g. "hk bdd my test name" or "hk regression", "hk lint" or "hk deploy").
* [seleniumdirector](https://github.com/hitchdev/seleniumdirector) -- tool that wraps selenium, making it easy to write simple, readable stories that interact with websites.
* [hitchbuildpy](https://github.com/hitchdev/hitchbuildpy) - tool that bundles pyenv and builds virtualenvs from it which can be used to install, run and test python code in one or many different versions.
* [hitchrunpy](https://github.com/hitchdev/hitchrunpy) - tool that can be used to run and monitor snippets of python code (can be used with hitchstory to write 'better unit tests' - for projects which provide a python API).
* [dirtemplate](https://github.com/hitchdev/dirtemplate) -- tool that generates a directory tree of text files from a directory tree of jinja2 templates - this can be used with hitchstory to autobuild documentation from stories.
* [hitchbuildpg](https://github.com/hitchdev/hitchbuildpg) -- tool that builds a local postgres database in a clearly defined state which can be used to develop or test with.
* [pretendsmtp](https://github.com/hitchdev/pretendsmtp) -- mock SMTP server which can be used to test code which sends emails via SMTP.

Coming soon:

* Mock REST server -- library to test code that calls REST APIs.
* interceptbrowser -- library to intercept browser traffic - can be used to intercept selenium browser traffic and modify browser headers, inject javascript (e.g. to mock time in the browser)
* hitchbuildmysql -- similar to hitchbuildpg but for mysql.
* hitchbuildredis -- build isolated redis server.
* hitchbuildnode -- build node environment.
* Suggestions welcome
