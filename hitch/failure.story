Simple failure report:
  description: |
    Basic failure report.
  preconditions:
    files:
      example.story: |
        Failing story:
          scenario:
            - Passing step
            - Failing step
            - Not executed step
      engine.py: |
        from hitchstory import BaseEngine
        from code_that_does_things import *


        class Engine(BaseEngine):
            def passing_step(self):
                pass

            def failing_step(self):
                raise_example_exception("Towel not located")

            def on_failure(self):
                reticulate_splines()

            def not_executed_step(self):
                pass
  scenario:
    - Run command: |
        from hitchstory import StoryCollection
        from engine import Engine
        from pathquery import pathq

        result = StoryCollection(pathq(".").ext("story"), Engine()).one().play()
        output(result.report())
    - Output will be:
        reference: failure
        changeable:
          - ((( anything )))/code_that_does_things.py
          - FAILURE IN ((( anything )))/example.story
          - ((( anything )))/story.py
          - ((( anything )))/engine.py
    - Splines reticulated
