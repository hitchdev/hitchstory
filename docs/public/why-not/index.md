---
title: Why not X?
---

There are a number of other ways of testing and documenting which might seem
very similar to hitchstory. I have tried to document how they differ and
why I chose hitchstory's approach here:

{% for dirfile in (thisdir.ext("md") - thisdir.named("index.md"))|sort() -%}
- [{{ title(dirfile) }}]({{ dirfile.basename().splitext()[0] }})
{% endfor %}

If you'd like to write or link to a rebuttal to any argument raised
here or ask for a comparison to something not listed here,
feel free to raise a ticket.
