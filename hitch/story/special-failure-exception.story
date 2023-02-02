Raising a Failure exception for known errors:
  docs: special-failure-exception
  about: |
    If you want to indicate a test failure, raise the
    "Failure" exception.

    This is by default an expected exception, so no stack trace
    will be printed if it is raised.
  given:
    files:
      engine.py: |
        from hitchstory import BaseEngine, no_stacktrace_for, Failure
        from code_that_does_things import raise_example_exception, output, ExampleException

        class Engine(BaseEngine):
            def passing_step(self):
                pass

            def failing_step(self):
                raise_example_exception("Towel not located")

            @no_stacktrace_for(ExampleException)
            def failing_step_without_stacktrace(self):
                raise_example_exception("Expected exception")

            def raise_special_failure_exception(self):
                raise Failure("Special failure exception - no stacktrace printed!")

            def step_that_will_not_run(self):
                pass
                
            def on_failure(self, result):
                pass

            def not_executed_step(self):
                pass
      example.story: |
        Failing story:
          steps:
            - Raise special failure exception
            - Step that will not run
            - Step that will not run
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathlib import Path

      story_collection = StoryCollection(Path(".").glob("*.story"), Engine())
  steps:
  - Run:
      code: story_collection.one().play()
      will output: |-
        RUNNING Failing story in /path/to/working/example.story ... FAILED in 0.1 seconds.

            Failing story:
              steps:
              - Raise special failure exception
              - Step that will not run
              - Step that will not run

        hitchstory.exceptions.Failure

            Test failed.

        Special failure exception - no stacktrace printed!
