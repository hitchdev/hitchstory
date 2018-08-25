HitchStory
==========

HitchStory is a python 3 library for building and running BDD-style executable specifications.

Unlike other BDD libraries the specification is written with [StrictYAML](https://hitchdev.com/strictyaml).

The specifications are designed to be simple to write, easy to read and to integrate seamlessly with the
code that executes them.

Hitchstory also lets you:

* Write parameterized stories and do property based testing.
* Generate documentation from your stories.
* Write stories that rewrite themselves.
* Write stories that inherit from one another.

This library was dogfooded for years to BDD, test and autodocument a variety
of different kinds of software - web apps, python libraries, command line apps, replacing
other forms of unit, integration and end to end tests.

Example
-------

{% for story in quickstart %}
{{ story.name }}:
{% if 'yaml_snippet' in story.data['given'] %}
```yaml
{{ story.given.yaml_snippet }}
```
{% endif %}
{% if 'setup' in story.data['given'] %}
```python
{{ story.given.setup }}
```
{% endif %}
{% endfor %}


Install
-------

To install:

  $ pip install hitchstory


Using HitchStory
----------------

{% for dirfile in subdir("using/alpha/").is_not_dir() - subdir("using/alpha/").named("index.md") -%}
- [{{ title(dirfile) }}](using/alpha/{{ dirfile.namebase }})
{% endfor %}


Tell me more
------------

HitchStory is a YAML based DSL for writing stories that is designed primarily to be ergonomic
for developers and only *incidentally* "`business readable <https://www.martinfowler.com/bliki/BusinessReadableDSL.html>`_".

By ergonomic for programmers, I mean:

* Stories can *and should* inherit from one another, because *specifications ought to be DRY too*.
* Stories are defined and validated using strongly typed StrictYAML. Step arguments and preconditions ('given') schemas can be defined by the programmer.
* The execution engine can be programmed to rewrite the executing story based upon program behavior changes (e.g. screen output changes, labels on a web app change).
* Running stories is done via a python API so you can easily write customized test workflows to suit your workflows.
* Story parameterization is built in.



Why not X instead?
------------------

* Why not just write unit tests (e.g with py.test)?
* Why not use Cucumber / Behat / Lettuce / pytest-bdd?
* Why not use robot framework?

{% for dirfile in subdir("why-not").is_not_dir() - subdir("why-not").named("index.md") -%} 
- [{{ title(dirfile) }}](why-not/{{ dirfile.namebase }})
{% endfor %}
