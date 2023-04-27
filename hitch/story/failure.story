Handling failing tests:
  docs: failing-tests
  about: |
    By default, a failing story will show:

    * A snippet of the YAML where the story failed with the failing step highlighted.
    * A stack trace from engine.py where the exception was raised.
  given:
    files:
      example.story: |
        Failing story:
          steps:
            - Passing step
            - Failing step
            - Not executed step
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
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathlib import Path

      story_collection = StoryCollection(Path(".").glob("*.story"), Engine())
  variations:
    Failure in set_up method:
      given:
        files:
          engine.py: |
            from hitchstory import BaseEngine
            from code_that_does_things import raise_example_exception

            class Engine(BaseEngine):
                def set_up(self):
                    raise_example_exception()
      steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            RUNNING Failing story in /path/to/working/example.story ... FAILED in 0.1 seconds.



            [1]: function 'set_up'
              /path/to/working/engine.py


                    3 : class Engine(BaseEngine):
                    4 :     def set_up(self):
                --> 5 :         raise_example_exception()
                    6 :



            [2]: function 'raise_example_exception'
              /path/to/working/code_that_does_things.py


                    21 :
                    22 : def raise_example_exception(text=""):
                --> 23 :     raise ExampleException(text)
                    24 :



            code_that_does_things.ExampleException

                This is a demonstration exception docstring.

                It spreads across multiple lines.

    Failure printed by default:
      steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            RUNNING Failing story in /path/to/working/example.story ... FAILED in 0.1 seconds.

                  steps:
                  - Passing step
                  - Failing step
                  - Not executed step


            [1]: function 'failing_step'
              /path/to/working/engine.py


                    6 :
                    7 :     def failing_step(self):
                --> 8 :         raise_example_exception("Towel not located")
                    9 :



            [2]: function 'raise_example_exception'
              /path/to/working/code_that_does_things.py


                    21 :
                    22 : def raise_example_exception(text=""):
                --> 23 :     raise ExampleException(text)
                    24 :



            code_that_does_things.ExampleException

                This is a demonstration exception docstring.

                It spreads across multiple lines.

            Towel not located
