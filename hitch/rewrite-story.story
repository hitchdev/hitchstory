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
          def __init__(self, rewrite=True):
              self._rewrite = rewrite

          def do_thing(self, variable):
              if self._rewrite:
                  self.current_step.update(
                      variable="xxx:\nyyy"
                  )

          def do_other_thing(self, variable1=None, variable2=None):
              if self._rewrite:
                  self.current_step.update(
                      variable2="complicated:\nmultiline\nstring"
                  )

          def on_success(self):
              self.new_story.save()
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine
  variations:
    No changes:
      steps:
      - Run:
          code: |
            result = StoryCollection(pathq(".").ext("story"), Engine(rewrite=False)).ordered_by_name().play()
            print(result.report())
      - File unchanged: example.story

    Rewritten:
      steps:
      - Run:
          code: |
            result = StoryCollection(pathq(".").ext("story"), Engine(rewrite=True)).ordered_by_name().play()
            print(result.report())
          will output: |-
            RUNNING Do things in /path/to/example.story ... SUCCESS in 0.1 seconds.
            RUNNING Do things/Do more things in /path/to/example.story ... SUCCESS in 0.1 seconds.
            SUCCESS in 0.1 seconds.
            SUCCESS in 0.1 seconds.

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
