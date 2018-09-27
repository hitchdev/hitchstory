{% if readme -%}
# HitchStory
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


## Example

{% for story in quickstart %}
{% with include_title=False %}{% include 'story.jinja2' %}{% endwith %}
{% endfor %}


## Installing

It's recommended to install and [set up hitchstory with hitchkey](setup-with-hitchkey), which can take care of automatically
setting up a up the [recommended hitchstory environment](approach/recommended-environment).

You can also install it traditionally through pypi:

```bash
$ pip install hitchstory
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
