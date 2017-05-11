Invalid YAML:
  description: |
    When a story has invalid YAML it will trigger
    a failure even when *other* stories are run.
    
    Names of stories and their filenames should
    be reported.
  preconditions:
    files:
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
  scenario:
    - Run command: |
        from hitchstory import StoryCollection
        from engine import Engine
        from pathquery import pathq

    - Assert Exception:
        command: StoryCollection(pathq(".").ext("story"), Engine()).named("Valid YAML").play()
        exception: example1.story
