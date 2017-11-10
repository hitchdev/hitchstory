Rewrite story:
  description: |
    Hitch stories can be rewritten in the event that you
    are dealing with generated blocks of text.
  given:
    example.story: |
      Do things:
        steps:
          - Do thing: x
          - Do thing: y
          - Do thing: z
          - Do other thing:
              variable1: a
              variable2: b

        variations:
          Do more things:
            steps:
              - Do thing: c
    engine.py: |
      from hitchstory import BaseEngine

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
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine
  steps:
  - Run:
      code: |
        result = StoryCollection(pathq(".").ext("story"), Engine()).ordered_by_name().play()
        print(result.report())
      will output: |-
        STORY RAN SUCCESSFULLY /path/to/example.story: Do things in 0.1 seconds.
        STORY RAN SUCCESSFULLY /path/to/example.story: Do things/Do more things in 0.1 seconds.

  - File contents will be:
      filename: example.story
      contents: |-
        Do things:
          steps:
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


          variations:
            Do more things:
              steps:
              - Do thing: |-
                  xxx:
                  yyy
