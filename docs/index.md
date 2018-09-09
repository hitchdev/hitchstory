HitchStory
==========

HitchStory is a python 3 library for building and running BDD-style executable specifications.

Unlike most other BDD tools which use Gherkin or SpecFlow the specification is written
with a dialect of [StrictYAML](https://hitchdev.com/strictyaml).

The specifications are designed to be simple to write, easy to read, to integrate seamlessly with the
code that executes them.

Hitchstory also lets you:

* Write parameterized stories and do property based testing.
* Generate documentation from your stories.
* Easily write code that rewrites stories (e.g. expected output) when code changes.
* Write stories that inherit from one another (for DRY stories).
* Test for story flakiness.

This library was dogfooded for years to TDD / BDD, test and autodocument a variety
of different kinds of software - web apps, python libraries, command line apps,
replacing other forms of unit, integration and end to end tests.

Example
-------

{% for story in quickstart %}
{% with include_title=False %}{% include 'story.jinja2' %}{% endwith %}
{% endfor %}


Install
-------

It's recommended to install and [set up hitchstory with hitchkey](setup-with-hitchkey), which can take care of auto-setting
up a python 3 virtualenv, installing other packages and providing an isolated directory which can be used to build code
and artefacts in.

Nonetheless, it is also possible to set up and use your own python 3 virtualenv and simply pip install hitchstory
from pypi.


Using HitchStory
----------------

{% for dirfile in subdir("using/alpha/").is_not_dir() - subdir("using/alpha/").named("index.md") -%}
- [{{ title(dirfile) }}](using/alpha/{{ dirfile.namebase }})
{% endfor %}


Recommended Complementary Tools
-------------------------------

This library was also designed alongside a number of other recommended tools which seamlessly
integrate with hitchstory, providing functionality to easily build and to test various different
kinds of software.

* [hitchkey](https://github.com/hitchdev/hitchkey) - create a project "key.py" of simple methods that can be used to run project-specific commands written in python directly from the command line (e.g. "hk bdd my test name" or "hk regression", "hk lint" or "hk deploy").
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

Tell me more
------------

HitchStory is a YAML based DSL for writing stories that is designed primarily to be ergonomic
for developers and only *incidentally* "[business readable](https://www.martinfowler.com/bliki/BusinessReadableDSL.html)".

By ergonomic for programmers, I mean:

* Stories can *and should* inherit from one another, because *specifications ought to be DRY too*.
* Stories are defined and validated using strongly typed StrictYAML. Step arguments and preconditions ('given') schemas can be defined by the programmer.
* The execution engine can be programmed to rewrite the executing story based upon program behavior changes (e.g. screen output changes, labels on a web app change).
* Running stories is done via a python API so you can easily write customized test workflows.
* Story parameterization is built in.



Why not X instead?
------------------

TODO : Section needs fleshing out more.

{% for dirfile in subdir("why-not").is_not_dir() - subdir("why-not").named("index.md") -%} 
- [{{ title(dirfile) }}](why-not/{{ dirfile.namebase }})
{% endfor %}
