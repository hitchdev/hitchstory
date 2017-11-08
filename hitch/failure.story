Simple failure report:
  description: |
    Basic failure report.
  given:
    example.story: |
      Failing story:
        steps:
          - Passing step
          - Failing step
          - Not executed step
    engine.py: |
      from hitchstory import BaseEngine, expected_exception, Failure
      from code_that_does_things import raise_example_exception, output, ExampleException

      class Engine(BaseEngine):
          def passing_step(self):
              pass

          def failing_step(self):
              raise_example_exception("Towel not located")

          @expected_exception(ExampleException)
          def failing_step_without_stacktrace(self):
              raise_example_exception("Expected exception")

          def raise_special_failure_exception(self):
              raise Failure("Special failure exception - no stacktrace printed!")

          def on_failure(self, result):
              print(result.report())

          def not_executed_step(self):
              pass
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathquery import pathq

      story_collection = StoryCollection(pathq(".").ext("story"), Engine())
  variations:
    Failure printed by on_failure method:
      steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            --> 8 :         raise_example_exception("Towel not located")
                    9 :



            [4]: function 'raise_example_exception'
              /path/to/code_that_does_things.py


                    20 :
                    21 : def raise_example_exception(text=""):
                --> 22 :     raise ExampleException(text)
                    23 :



            code_that_does_things.ExampleException

                This is a demonstration exception's docstring.

                It spreads across multiple lines.

            Towel not located
    Failure printed by default:
      steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            --> 8 :         raise_example_exception("Towel not located")
                    9 :



            [4]: function 'raise_example_exception'
              /path/to/code_that_does_things.py


                    20 :
                    21 : def raise_example_exception(text=""):
                --> 22 :     raise ExampleException(text)
                    23 :



            code_that_does_things.ExampleException

                This is a demonstration exception's docstring.

                It spreads across multiple lines.

            Towel not located

    Expected exception:
      description: |
        For common expected failures where you do not want
        to see the whole stacktrace.
      given:
        example.story: |
          Failing story:
            steps:
              - Failing step without stacktrace
      steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            FAILURE IN /path/to/example.story:
                "Failing story" in 0.1 seconds.


                Failing story:
                  steps:
                  - Failing step without stacktrace



            code_that_does_things.ExampleException

                This is a demonstration exception's docstring.

                It spreads across multiple lines.

            Expected exception


    Special exception named failure:
      description: |
        If you want to indicate a test failure, raise the
        "Failure" exception.

        This is by default an expected exception, so no stack trace
        will be printed if it is raised.
      given:
        example.story: |
          Failing story:
            steps:
              - Raise special failure exception
      steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            FAILURE IN /path/to/example.story:
                "Failing story" in 0.1 seconds.


                Failing story:
                  steps:
                  - Raise special failure exception



            hitchstory.exceptions.Failure

                Test failed.

            Special failure exception - no stacktrace printed!
