Match two strings and show diff on failure:
  docs: engine/match-two-strings
  based on: handling failing tests
  about: |
    While you could use `assert expected == actual` to match
    two strings in a story step, if you use `should_match(expected, actual)`
    instead then when it fails:

    * It will show the actual string, expected string *and a diff*.
    * It will raise a Failure exception and avoid polluting the error message with the full stacktrace.

    An example is shown below:
  given:
    files:
      example.story: |
        Failing story:
          steps:
            - Pass because strings match
            - Fail because strings don't match
      engine.py: |
        from hitchstory import BaseEngine, strings_match

        class Engine(BaseEngine):
            def pass_because_strings_match(self):
                strings_match("hello", "hello")

            def fail_because_strings_dont_match(self):
                strings_match("hello", "goodbye")
  
  steps:
  - Run:
      code: story_collection.one().play()
      will output: |-
        RUNNING Failing story in /path/to/working/example.story ... FAILED in 0.1 seconds.

              steps:
              - Pass because strings match
              - Fail because strings don't match


        hitchstory.exceptions.Failure

            Test failed.

        ACTUAL:
        goodbye

        EXPECTED:
        hello

        DIFF:
        - hello+ goodbye
