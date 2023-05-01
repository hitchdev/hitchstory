Hiding stacktraces for expected exceptions:
  docs: engine/expected-exceptions
  based on: handling failing tests
  about: |
    For common and expected exceptions where you do not want
    the entire stacktrace to be spewed out in the error message,
    you can apply the "@no_stacktrace_for" decorator to the step.
    
    See also:
    
    * [Raise a Failure exception](../special-failure-exception)
    * [Compare two strings](../match-two-strings)
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

            Failing story:
              steps:
              - Failing step without stacktrace


        code_that_does_things.ExampleException

            This is a demonstration exception docstring.

            It spreads across multiple lines.

        Expected exception
