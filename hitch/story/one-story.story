Run one story in collection:
  docs: runner/run-just-one-story
  about: |
    If you have just one story in your collection,
    you can run it directly by using .one().
  given:
    files:
      example.story: |
        Do thing:
          steps:
            - Do thing
      engine.py: |
        from hitchstory import BaseEngine
        from code_that_does_things import *

        class Engine(BaseEngine):
            def do_thing(self):
                pass
    setup: |
      from hitchstory import StoryCollection
      from pathlib import Path
      from engine import Engine


      story = StoryCollection(Path(".").glob("*.story"), Engine()).one()
  steps:
  - Run:
      code: story.play()
      will output: RUNNING Do thing in /path/to/working/example.story ... SUCCESS
        in 0.1 seconds.
