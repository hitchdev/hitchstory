
---
title: Flaky story detection
type: using
---



Dealing with flaky stories, especially with higher level integration tests
is a constant battle.

These examples show how flaky stories can be detected by rerunning stories
several times and checking that the result is the same. This kind of regression
testing can be usefully run separately from normal regression testing in order
to get separate feedback about problematic tests in a 'flake' report.

This cannot detect all kinds of flakiness, but it can be effective at detecting
flakiness caused by, for example:

* SELECT statements without an order by returning results in an arbitrary order.
* Data structures with an indeterminate order (e.g. hash maps (python dicts)) being listed.
* Stories that result in random numbers being generated and used.
* Race conditions.
* Web page responsiveness (e.g. a selenium click that is done too quickly).

Note that a flakiness "pass" is simply about whether results are *consistent* - a story that
fails consistently is considered passed, whereas a story that is run 99 times and fails once
is considered a failure.






example1.story:

```yaml
Flaky story:
  steps:
  - Step that fails on fifth run

Consistent failure:
  steps:
  - Step that always fails

```










```python
from hitchstory import StoryCollection, BaseEngine, Failure
from pathquery import pathquery

class Engine(BaseEngine):
    def __init__(self):
        self._tries = 0

    def step_that_fails_on_fifth_run(self):
        self._tries = self._tries + 1
        if self._tries >= 5:
            raise Failure("Flaky story failure!")

    def step_that_always_fails(self):
        raise Failure("Consistent failure!")

```




Run a single story that fails on fifth try:




```python
flake_result = StoryCollection(pathquery(".").ext("story"), Engine()).with_flake_detection(times=5).named("flaky story").play()

assert flake_result.is_flaky

```

Will output:
```
RUNNING Flaky story in /path/to/example1.story ... SUCCESS in 0.1 seconds.
RUNNING Flaky story in /path/to/example1.story ... SUCCESS in 0.1 seconds.
RUNNING Flaky story in /path/to/example1.story ... SUCCESS in 0.1 seconds.
RUNNING Flaky story in /path/to/example1.story ... SUCCESS in 0.1 seconds.
RUNNING Flaky story in /path/to/example1.story ... FAILED in 0.1 seconds.

    Flaky story:
      steps:
      - Step that fails on fifth run

    Consistent failure:

hitchstory.exceptions.Failure

    Test failed.

Flaky story failure!

FLAKINESS DETECTED in 0.1 seconds, 20% of stories failed.
```






Run a single story that fails every time:




```python
flake_result = StoryCollection(pathquery(".").ext("story"), Engine()).with_flake_detection(times=5).named("consistent failure").play()

assert not flake_result.is_flaky

```

Will output:
```
RUNNING Consistent failure in /path/to/example1.story ... FAILED in 0.1 seconds.

    Consistent failure:
      steps:
      - Step that always fails


hitchstory.exceptions.Failure

    Test failed.

Consistent failure!
RUNNING Consistent failure in /path/to/example1.story ... FAILED in 0.1 seconds.

    Consistent failure:
      steps:
      - Step that always fails


hitchstory.exceptions.Failure

    Test failed.

Consistent failure!
RUNNING Consistent failure in /path/to/example1.story ... FAILED in 0.1 seconds.

    Consistent failure:
      steps:
      - Step that always fails


hitchstory.exceptions.Failure

    Test failed.

Consistent failure!
RUNNING Consistent failure in /path/to/example1.story ... FAILED in 0.1 seconds.

    Consistent failure:
      steps:
      - Step that always fails


hitchstory.exceptions.Failure

    Test failed.

Consistent failure!
RUNNING Consistent failure in /path/to/example1.story ... FAILED in 0.1 seconds.

    Consistent failure:
      steps:
      - Step that always fails


hitchstory.exceptions.Failure

    Test failed.

Consistent failure!

NO FLAKINESS DETECTED in 0.1 seconds after running 'Consistent failure' story 5 times.
```










{{< note title="Executable specification" >}}
Page automatically generated from <a href="https://github.com/hitchdev/hitchstory/blob/master/hitch/flaky.story">flaky.story</a>.
{{< /note >}}
