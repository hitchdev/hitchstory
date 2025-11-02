Exceptions when matching JSON:
  based on: match two json snippets
  given:
    files:
      example.story: |
        Failing story:
          steps:
            - Failing step
  variations:
    Expected is an int:
      given:
        files:
          engine.py: |
            from hitchstory import BaseEngine, json_match

            class Engine(BaseEngine):
                def failing_step(self):
                    json_match(
                        4,
                        """{"x": 3}"""
                    )
      replacement steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            RUNNING Failing story in /path/to/working/example.story ... FAILED in 0.1 seconds.

                Failing story:
                  steps:
                  - Failing step


            hitchstory.exceptions.Failure

            Test failed.

            json_match(expected, actual) - expected should bea string, instead it is of type <class 'int'>.

    Expected is dict:
      given:
        files:
          engine.py: |
            from hitchstory import BaseEngine, json_match

            class Engine(BaseEngine):
                def failing_step(self):
                    json_match(
                        {"x": 3},
                        """{"x": 3}"""
                    )
      replacement steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            RUNNING Failing story in /path/to/working/example.story ... FAILED in 0.1 seconds.

                Failing story:
                  steps:
                  - Failing step


            hitchstory.exceptions.Failure

            Test failed.

            json_match(expected, actual) - expected is a dict. It should be a string of unparsed JSON.

            You could try sending the original JSON string or use json.dumps(the_dict)

    Actual not JSON:
      given:
        files:
          engine.py: |
            from hitchstory import BaseEngine, json_match

            class Engine(BaseEngine):
                def failing_step(self):
                    json_match(
                        """{"b": 2, "a": 1}""",
                        """Not JSON"""
                    )
      replacement steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            RUNNING Failing story in /path/to/working/example.story ... FAILED in 0.1 seconds.

                Failing story:
                  steps:
                  - Failing step


            hitchstory.exceptions.Failure

            Test failed.

            json_match(expected, actual) - actual value is not valid JSON:

            Not JSON

    Expected not JSON:
      given:
        files:
          engine.py: |
            from hitchstory import BaseEngine, json_match

            class Engine(BaseEngine):
                def failing_step(self):
                    json_match(
                        """Not JSON""",
                        """{"b": 2, "a": 1}"""
                    )
      replacement steps:
      - Run:
          code: story_collection.one().play()
          will output: |-
            RUNNING Failing story in /path/to/working/example.story ... FAILED in 0.1 seconds.

                Failing story:
                  steps:
                  - Failing step


            hitchstory.exceptions.Failure

            Test failed.

            json_match(expected, actual) - expected value is not valid JSON:

            Not JSON
