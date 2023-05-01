Hiding stacktraces for expected exceptions:
  category: engine
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

            Failing story:
              steps:
              - Failing step without stacktrace


        code_that_does_things.ExampleException

            This is a demonstration exception docstring.

            It spreads across multiple lines.

        Expected exception
