Hiding stacktraces for expected exceptions:
  docs: expected-exceptions
  based on: handling failing tests
  about: |
    For common expected failures where you do not want
    to see the whole stacktrace, apply the "@no_stacktrace_for"
    decorator.
  given:
    files:
      example.story: |
        Failing story:
          steps:
            - Failing step without stacktrace
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
