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

        variations:
          Do more things:
            scenario:
              - Do thing: c
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
      result = StoryCollection(pathq(".").ext("story"), Engine()).ordered_by_name().play()
      output(result.report())
  scenario:
  - Run code
  - Output is: |
      STORY RAN SUCCESSFULLY ((( anything )))/example.story: Do things in ((( anything ))) seconds.
      STORY RAN SUCCESSFULLY ((( anything )))/example.story: Do things/Do more things in ((( anything ))) seconds.
  - File contents will be:
      filename: example.story
      contents: "Do things:\n  scenario:\n  - Do thing: |-\n      xxx:\n      yyy\n\
        \  - Do thing: |-\n      xxx:\n      yyy\n  - Do thing: |-\n      xxx:\n \
        \     yyy\n  - Do other thing:\n      variable1: a\n      variable2: |-\n\
        \        complicated:\n        multiline\n        string\n               \
        \    \n\n  variations:\n    Do more things:\n      scenario:\n      - Do thing:\
        \ |-\n          xxx:\n          yyy"
