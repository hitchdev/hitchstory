Invalid YAML:
  about: |
    When a story has invalid YAML it will trigger
    a failure even when *other* stories are run.

    Names of stories and their filenames should
    be reported.
  given:
    files:
      example1.story: |
        Invalid YAML:
          steps
            - Do something
                note the ^^^^ invalid YAML
      example2.story: |
        Valid YAML:
          steps:
            - Do something: |
                text
      example3.story: |
        Invalid YAML:
          steps:
            - Do something: text
      engine.py: |
        from hitchstory import BaseEngine

        class Engine(BaseEngine):
            def do_something(self, text):
                pass
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathquery import pathquery
  steps:
  - Run:
      code: |
        StoryCollection(pathquery(".").ext("story"), Engine()).named("Valid YAML").play()
      raises:
        type: hitchstory.exceptions.StoryYAMLError
        message: |-
          YAML Error in file '/path/to/working/example1.story':
          when expecting a mapping
          found arbitrary text
            in "<unicode string>", line 1, column 1:
              Invalid YAML: steps - Do somethin ...
               ^ (line: 1)
