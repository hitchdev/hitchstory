---
title: Design Justifications
---

HitchStory is the result of some carefully considered, although
controversial design decisions. These are justified here.

{% for dirfile in thisdir.is_not_dir() - thisdir.named("index.md") -%}
- [{{ title(dirfile) }}]({{ dirfile.namebase }})
{% endfor %}

Rebuttals and critiques, especially from users and designers of 
competing tools are welcome. Either raise a ticket on github
or open a pull request with a link.
