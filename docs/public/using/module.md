---
title: Module
---
# Module

Use a python module with template variables and methods.





note.org
```
* Note 1

* Note 2

```


note.jinja2
```
{% for note in root %}
{{ to_upper(note.name) }}
{% endfor %}

```


note.py
```
def to_upper(string):
    return string.upper()

```




orji --module note.py note.org note.jinja2


```

NOTE 1

NOTE 2


```
