Invalid YAML:
  description: |
    When a story has invalid YAML it will trigger
    a failure even when *other* stories are run.

    Names of stories and their filenames should
    be reported.
  given:
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
          Invalid
    engine.py: |
      from hitchstory import BaseEngine

      class Engine(BaseEngine):
          def do_something(self, text):
              pass
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathquery import pathq
  steps:
  - Run:
      code: |
        StoryCollection(pathq(".").ext("story"), Engine()).named("Valid YAML").play()
      raises:
        type: hitchstory.exceptions.StoryYAMLError
        message: "YAML Error in file '/path/to/example3.story':\nwhile scanning a\
          \ simple key\n  in \"<unicode string>\", line 4, column 5:\n        Invalid\n\
          \        ^ (line: 4)\ncould not find expected ':'\n  in \"<unicode string>\"\
          , line 5, column 1:\n\n    ^ (line: 5)"
