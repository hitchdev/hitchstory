Simple failure report:
  about: |
    A basic failure report gives an output that includes a snippet
    of the step YAML story with the failing step highlighted and 
    a stack trace in the engine where the exception was raised.
  given:
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
      from pathquery import pathq

      story_collection = StoryCollection(pathq(".").ext("story"), Engine())
  variations:
    Failure in set_up method:
      given:
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
            RUNNING Failing story in /path/to/example.story ... FAILED in 0.1 seconds.



            [1]: function 'set_up'
              /path/to/engine.py


                    3 : class Engine(BaseEngine):
                    4 :     def set_up(self):
                --> 5 :         raise_example_exception()
                    6 :



            [2]: function 'raise_example_exception'
              /path/to/code_that_does_things.py


                    20 :
                    21 : def raise_example_exception(text=""):
                --> 22 :     raise ExampleException(text)
                    23 :



            code_that_does_things.ExampleException

                This is a demonstration exception docstring.

                It spreads across multiple lines.

    Failure printed by default:
      steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            RUNNING Failing story in /path/to/example.story ... FAILED in 0.1 seconds.

                  steps:
                  - Passing step
                  - Failing step
                  - Not executed step


            [1]: function 'failing_step'
              /path/to/engine.py


                    6 :
                    7 :     def failing_step(self):
                --> 8 :         raise_example_exception("Towel not located")
                    9 :



            [2]: function 'raise_example_exception'
              /path/to/code_that_does_things.py


                    20 :
                    21 : def raise_example_exception(text=""):
                --> 22 :     raise ExampleException(text)
                    23 :



            code_that_does_things.ExampleException

                This is a demonstration exception docstring.

                It spreads across multiple lines.

            Towel not located

    Expected exception:
      about: |
        For common expected failures where you do not want
        to see the whole stacktrace, apply the "@no_stacktrace_for"
        decorator.
      given:
        example.story: |
          Failing story:
            steps:
              - Failing step without stacktrace
      steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            RUNNING Failing story in /path/to/example.story ... FAILED in 0.1 seconds.

                Failing story:
                  steps:
                  - Failing step without stacktrace


            code_that_does_things.ExampleException

                This is a demonstration exception docstring.

                It spreads across multiple lines.

            Expected exception


    Special exception named failure:
      about: |
        If you want to indicate a test failure, raise the
        "Failure" exception.

        This is by default an expected exception, so no stack trace
        will be printed if it is raised.
      given:
        example.story: |
          Failing story:
            steps:
              - Raise special failure exception
              - Step that will not run
              - Step that will not run
      steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            RUNNING Failing story in /path/to/example.story ... FAILED in 0.1 seconds.

                Failing story:
                  steps:
                  - Raise special failure exception
                  - Step that will not run
                  - Step that will not run

            hitchstory.exceptions.Failure

                Test failed.

            Special failure exception - no stacktrace printed!
