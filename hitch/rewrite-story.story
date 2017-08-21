Rewrite story:
  description: |
    Hitch stories can be rewritten in the event that you
    are dealing with generated blocks of text.
  preconditions:
    example.story: |
      Do things:
        scenario:
          - Do thing: x
          - Do thing: y
          - Do thing: z
          - Do other thing:
              variable1: a
              variable2: b
    engine.py: |
      from hitchstory import BaseEngine
      from code_that_does_things import *

      class Engine(BaseEngine):
          def do_thing(self, variable):
              self.current_step.update(
                  variable="xxx:\nyyy"
              )

          def do_other_thing(self, variable1=None, variable2=None):
              self.current_step.update(
                  variable2="complicated:\nmultiline\nstring"
              )

          def on_success(self):
              self.new_story.save()
    setup: |
      from code_that_does_things import *
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine

    code: |
      result = StoryCollection(pathq(".").ext("story"), Engine()).named("Do things").play()
      output(result.report())
  scenario:
    - Run code
    - Output is: |
        STORY RAN SUCCESSFULLY ((( anything )))/example.story: Do things in 0.1 seconds.
    - File contents will be:
        filename: example.story
        contents: |
          Do things:
            scenario:
            - Do thing: |-
                xxx:
                yyy
            - Do thing: |-
                xxx:
                yyy
            - Do thing: |-
                xxx:
                yyy
            - Do other thing:
                variable1: a
                variable2: |-
                  complicated:
                  multiline
                  string
