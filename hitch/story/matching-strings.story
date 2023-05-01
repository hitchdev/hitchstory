Match two strings:
  category: engine
  docs: match-two-strings
  based on: handling failing tests
  about: |
    Where two strings should match you can use
    should_match(expected, actual) to compare them.
    
    If they don't match, a Failure exception with
    the expected, actual and a diff between the two
    will be printed for debugging purposes.
    
    This makes it slightly more helpful than
    assert expected == actual.
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
