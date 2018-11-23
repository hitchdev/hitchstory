{% if readme -%}
# HitchStory
{%- else -%}

---
title: HitchStory
---

![You know why](sliced-cucumber.jpg)

{% raw %}{{< github-stars user="hitchdev" project="hitchstory" >}}{% endraw %}
{% endif %}


HitchStory is a python 3
[testing and living documentation framework](approach/testing-and-living-documentation) for building easily
maintained example driven [executable specifications](approach/executable-specifications) (sometimes dubbed
acceptance tests).

It was designed initially to make [realistic testing](approach/test-realism) of code less
of a goddamn chore so the tests would actually get written and run.

The executable specifications can be written to specify and test applications at
any level and have been used successfully to replace traditional
[low level unit tests](), [integration tests]() and [end to end tests]()
with easier to maintain tests.

The specifications are [written using StrictYAML](why/strictyaml) and the
code to execute them is written by you, in python.


## Example

{% for story in quickstart %}
{% with include_title=False %}{% include 'story.jinja2' %}{% endwith %}
{% endfor %}


## Installation and set up

You *can* install hitchstory through pypi in any python 3 virtualenv:

```bash
$ pip install hitchstory
```

However, it's recommended to install and set up hitchstory with [hitchkey](https://github.com/hitchdev/hitchkey),
which will take care of automatically setting up a up the [recommended hitchstory environment](approach/recommended-environment).

Either install hitchkey with [pipsi](https://github.com/mitsuhiko/pipsi):

```bash
pipsi install hitchkey
```

Or, if you'd prefer, you can safely install with "sudo pip":

```bash
sudo pip install hitchkey
```

Once hitchkey is installed:

```bash
cd /your/project/directory
hk --tutorial hitchstory
```

This will create a directory called "hitch" and put three files in it, including one story, which you can play by running:

```bash
hk bdd my first
```


## Using HitchStory

{% for dirfile in subdir("using/alpha/").is_not_dir() - subdir("using/alpha/").named("index.md") -%}
- [{{ title(dirfile) }}](using/alpha/{{ dirfile.namebase }})
{% endfor %}


## Approach to using HitchStory

Best practices, how the tool was meant to be used, etc.

{% for dirfile in subdir("approach").is_not_dir() - subdir("approach").named("index.md") -%} 
- [{{ title(dirfile) }}](approach/{{ dirfile.namebase }})
{% endfor %}

## Design decisions and principles

Somewhat controversial design decisions are justified here.

{% for dirfile in subdir("why").is_not_dir() - subdir("why").named("index.md") -%} 
- [{{ title(dirfile) }}](why/{{ dirfile.namebase }})
{% endfor %}

## Why not X instead?

There are several tools you can use instead, this is why you should use this one instead:

{% for dirfile in subdir("why-not").is_not_dir() - subdir("why-not").named("index.md") -%} 
- [{{ title(dirfile) }}](why-not/{{ dirfile.namebase }})
{% endfor %}
