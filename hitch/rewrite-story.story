Rewrite story:
  description: |
    Hitch stories can be rewritten in the event that you
    are dealing with generated blocks of text.
  preconditions:
    files:
      example.story: |
        Do things:
          scenario:
            - Do thing: x
            - Do thing: y
            - Do thing: z
      engine.py: |
        from hitchstory import BaseEngine
        from code_that_does_things import *


        class Engine(BaseEngine):
            def do_thing(self, variable):
                self.current_step.update(
                    variable="xxx"
                )

            def on_success(self):
                self.new_story.save()
  scenario:
    - Run command: |
        from hitchstory import StoryCollection
        from pathquery import pathq
        from engine import Engine

        result = StoryCollection(pathq(".").ext("story"), Engine()).named("Do things").play()
        output(result.report())
    - Output is: |
        STORY RAN SUCCESSFULLY ((( anything )))/example.story: Do things in 0.1 seconds.
    - File contents will be:
        filename: example.story
        contents: |
          Do things:
            scenario:
            - Do thing: xxx
            - Do thing: xxx
            - Do thing: xxx
