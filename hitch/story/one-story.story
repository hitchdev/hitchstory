Run one story in collection:
  about: |
    If you have just one story in your collection,
    you can run it directly by using .one().
  given:
    example.story: |
      Do thing:
        steps:
          - Do thing
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathquery
      from engine import Engine


      story = StoryCollection(pathquery(".").ext("story"), Engine()).one()
    engine.py: |
      from hitchstory import BaseEngine
      from code_that_does_things import *

      class Engine(BaseEngine):
          def do_thing(self):
              pass
  steps:
  - Run:
      code: story.play()
      will output: RUNNING Do thing in /path/to/working/example.story ... SUCCESS
        in 0.1 seconds.
