---
title: Deliberately fail
---
# Deliberately fail

When your template has an error condition that
you need to raise, use fail("error message")
to raise the error.





example.org
```
* existent

```


example.jinja2
```
This is some text

{{ fail("this shouldn't happen") }}

This is some more text.

```




orji example.org example.jinja2

Will error with:
```
Failure on line 3 of example.jinja2: this shouldn't happen

```
