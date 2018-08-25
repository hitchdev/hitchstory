Special exception named failure:
  based on: handling failing tests
  docs: special-failure-exception
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
