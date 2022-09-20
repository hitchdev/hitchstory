Flaky story detection:
  docs: flaky-story-detection
  about: |
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
  given:
    core files:
      example1.story: |
        Flaky story:
          steps:
          - Step that fails on fifth run

        Consistent failure:
          steps:
          - Step that always fails
    setup: |
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
  variations:
    Run a single story that fails on fifth try:
      steps:
      - Run:
          code: |
            flake_result = StoryCollection(pathquery(".").ext("story"), Engine()).with_flake_detection(times=5).named("flaky story").play()

            assert flake_result.is_flaky
          will output: |-
            RUNNING Flaky story in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
            RUNNING Flaky story in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
            RUNNING Flaky story in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
            RUNNING Flaky story in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.
            RUNNING Flaky story in /path/to/working/example1.story ... FAILED in 0.1 seconds.

                Flaky story:
                  steps:
                  - Step that fails on fifth run

                Consistent failure:

            hitchstory.exceptions.Failure

                Test failed.

            Flaky story failure!

            FLAKINESS DETECTED in 0.1 seconds, 20% of stories failed.

    Run a single story that fails every time:
      steps:
      - Run:
          code: |
            flake_result = StoryCollection(pathquery(".").ext("story"), Engine()).with_flake_detection(times=5).named("consistent failure").play()

            assert not flake_result.is_flaky
          will output: |-
            RUNNING Consistent failure in /path/to/working/example1.story ... FAILED in 0.1 seconds.

                Consistent failure:
                  steps:
                  - Step that always fails


            hitchstory.exceptions.Failure

                Test failed.

            Consistent failure!
            RUNNING Consistent failure in /path/to/working/example1.story ... FAILED in 0.1 seconds.

                Consistent failure:
                  steps:
                  - Step that always fails


            hitchstory.exceptions.Failure

                Test failed.

            Consistent failure!
            RUNNING Consistent failure in /path/to/working/example1.story ... FAILED in 0.1 seconds.

                Consistent failure:
                  steps:
                  - Step that always fails


            hitchstory.exceptions.Failure

                Test failed.

            Consistent failure!
            RUNNING Consistent failure in /path/to/working/example1.story ... FAILED in 0.1 seconds.

                Consistent failure:
                  steps:
                  - Step that always fails


            hitchstory.exceptions.Failure

                Test failed.

            Consistent failure!
            RUNNING Consistent failure in /path/to/working/example1.story ... FAILED in 0.1 seconds.

                Consistent failure:
                  steps:
                  - Step that always fails


            hitchstory.exceptions.Failure

                Test failed.

            Consistent failure!

            NO FLAKINESS DETECTED in 0.1 seconds after running 'Consistent failure' story 5 times.
