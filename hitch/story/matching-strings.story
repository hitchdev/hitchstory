Match two strings and show diff on failure:
  docs: engine/match-two-strings
  based on: handling failing tests
  about: |
    While you could use `assert expected == actual` to match
    two strings in a story step, if you use `should_match(expected, actual)`
    instead then when it fails:
    
    * It will show the actual string, expected string *and the diff*.
    * It will raise a Failure exception and avoid polluting the error message with the full stacktrace.
    
    An example is shown below:
  given:
    files:
      example.story: |
        Failing story:
          steps:
            - Fail because strings don't match
  steps:
  - Run:
      code: story_collection.one().play()
      will output: |-
        RUNNING Failing story in /path/to/working/example.story ... FAILED in 0.1 seconds.

            Failing story:
              steps:
              - Fail because strings don't match


        hitchstory.exceptions.Failure

            Test failed.

        ACTUAL:
        goodbye

        EXPECTED:
        hello

        DIFF:
        - hello+ goodbye
