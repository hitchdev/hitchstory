---
title: Why does hitchstory not have a command line interface?
---

One of the main irritations I found with other testing frameworks
was the lack of flexibility regarding which tests were run, how
they are run and in which order and how they are run.

Moreover, I have almost always ended up creating quite elaborate
code that calls the tests and runs them in the manner and order
I wanted.

HitchStory pre-empts that step and *requires* you to write code in
order to run your tests. It might just be a one liner, but since
the code is one line and is code, it's a highly configurable one
liner which will likely be changed.

HitchStory is furthermore designed to run in a separate code
environment (virtualenv). The natural way to use it is with
hitchkey which takes care of setting up a virtual environment,
installing all necessary testing packages (including hitchstory),
keeping them up to date, and providing an easily accessible
directory to put build artefacts in.

Example hitchkey key.py code to run a single test from
[this project](https://github.com/crdoconnor/strictyaml):

```python
@expected(HitchStoryException)
def bdd(*keywords):
    """
    Run story matching keywords.
    """
    settings = _personal_settings().data
    _storybook(settings["engine"]).with_params(
        **{"python version": settings["params"]["python version"]}
    ).only_uninherited().shortcut(*keywords).play()
```

Example hitchkey key.py code to lint, run all doctests and all stories
with python 2.7 and 3.7:


```python
@expected(HitchStoryException)
def regression():
    """
    Run regression testing - lint and then run all tests.
    """
    lint()
    doctests()
    storybook = _storybook({}).only_uninherited()
    storybook.with_params(**{"python version": "2.7.14"}).filter(
        lambda story: not story.info.get("fails_on_python_2")
    ).ordered_by_name().play()
    storybook.with_params(**{"python version": "3.7.0"}).ordered_by_name().play()
```


Example hitchkey key.py code to run a single test in [rewrite mode](../rewrite):

```python
@expected(HitchStoryException)
def rbdd(*keywords):
    """
    Run story matching keywords and rewrite story if code changed.
    """
    settings = _personal_settings().data
    settings["engine"]["rewrite"] = True
    _storybook(settings["engine"]).with_params(
        **{"python version": settings["params"]["python version"]}
    ).only_uninherited().shortcut(*keywords).play()
```

