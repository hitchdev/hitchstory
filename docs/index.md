{% if readme -%}
HitchStory
==========
{%- else -%}

---
title: HitchStory
---

![You know why](sliced-cucumber.jpg)

{% raw %}{{< github-stars user="hitchdev" project="hitchstory" >}}{% endraw %}
{% endif %}


HitchStory is a python 3 library for creating readable "specifications by example" and executing
them. It is an ambitious project intended supplant both traditional BDD tools and unit tests.

Unlike many other BDD tools the specification is [written using StrictYAML](why/strictyaml) which
means that stories will be terse, strongly typed and expressive enough to describe business
rules and behavior in precise detail.


Example
-------

{% for story in quickstart %}
{% with include_title=False %}{% include 'story.jinja2' %}{% endwith %}
{% endfor %}


Install
-------

It's recommended to install and [set up hitchstory with hitchkey](setup-with-hitchkey), which can take care of automatically
setting up a up the [recommended hitchstory environment](approach/recommended-environment).

You can also install it traditionally through pypi:

```bash
$ pip install hitchstory
```


Using HitchStory
----------------

{% for dirfile in subdir("using/alpha/").is_not_dir() - subdir("using/alpha/").named("index.md") -%}
- [{{ title(dirfile) }}](using/alpha/{{ dirfile.namebase }})
{% endfor %}


Tell me more
------------

HitchStory is a YAML based DSL for writing story 'specifications', designed to be simple to write, easy to read, to integrate seamlessly with the
code that executes them.

This library was dogfooded for years to TDD / BDD, test and autodocument a variety
of different kinds of software - web apps, python libraries, command line apps,
replacing all other forms of unit, integration and end to end tests.

Unlike traditional "BDD" frameworks like Cucumber, hitchstory is not primarily designed for
"[business readability](https://www.martinfowler.com/bliki/BusinessReadableDSL.html)",
but rather for simplicity ease of maintenance by developers.

This means:

* Stories can *and should* inherit from one another, because *specifications ought to be DRY too*.
* Stories are defined and validated using strongly typed StrictYAML. Step arguments and precondition ('given') schemas can be strictly defined by the programmer.
* The execution engine can be programmed to rewrite the executing story based upon certain kinds of behavior changes (e.g. output strings, screen output changes, messages in a web app).
* Running stories is done via a python API rather than the command line so you can easily program customized test workflows.
* There is built  in story parameterization so you can do property based testing.
* Stories can be easily tested for flakiness.
* The stories are designed to be easily used to build readable documentation.



Recommended Complementary Tools
-------------------------------

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


Design decisions
----------------

TODO : Needs fleshing out.

* Why inheritance

Why not X instead?
------------------

TODO : Section needs fleshing out more.

{% for dirfile in subdir("why-not").is_not_dir() - subdir("why-not").named("index.md") -%} 
- [{{ title(dirfile) }}](why-not/{{ dirfile.namebase }})
{% endfor %}
