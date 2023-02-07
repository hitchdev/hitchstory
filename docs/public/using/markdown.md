---
title: Markdown
---
# Markdown

Convert chunks of orgmode text into markdown using .body.markdown.





markdown.org
```
* Note title

Text with /emphasis/ and *bold* and a [[link][https://www.google]].

+ Bullet one
+ Bullet two

```


markdown.jinja2
```
{{ root.at("Note title").body.markdown }}

```




orji markdown.org markdown.jinja2


```

Text with /emphasis/ and *bold* and a [link](https://www.google).

* Bullet one
* Bullet two

```
