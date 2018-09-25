---
title: I see given but where is when and then?
---

You can certainly write user stories using when and then like so:

```yaml
Given:
  I have: red box
Steps:
  - When I click: the red button
  - Then it goes kaboom
```

However, hitchstory does not require this, and it is not generally encouraged
because, as with code, terseness and ease of editing is of primary importance
and this languge is designed for use primarily by programmers.

Writing the story like this is terser and no less clear:

```yaml
given:
  box: red
steps:
  - click: red button
  - goes kaboom
```

Where stakeholders wish to read documentation that is longer form and more
flowing, the latter can still be used to generate it.
