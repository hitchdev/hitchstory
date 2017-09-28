Invalid YAML:
  description: |
    When a story has invalid YAML it will trigger
    a failure even when *other* stories are run.

    Names of stories and their filenames should
    be reported.
  preconditions:
    example1.story: |
      Invalid YAML:
        scenario
          - Do something
              note the ^^^^ invalid YAML
    example2.story: |
      Valid YAML:
        scenario:
          - Do something: |
              text
    engine.py: |
      from hitchstory import BaseEngine
      from code_that_does_things import *


      class Engine(BaseEngine):
          def do_something(self, text):
              pass
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathquery import pathq
    code: |
      StoryCollection(pathq(".").ext("story"), Engine()).named("Valid YAML").play()
  scenario:
  - Raises exception: "YAML Error in file '/home/colm/.hitch/90646u/state/example1.story':\n\
      when expecting a mapping\nfound non-mapping\n  in \"<unicode string>\", line\
      \ 1, column 1:\n    Invalid YAML: scenario - Do somet ... \n     ^ (line: 1)"
