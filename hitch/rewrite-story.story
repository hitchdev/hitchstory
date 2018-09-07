Story that rewrites itself:
  docs: rewrite-story
  about: |
    Hitch stories can be partially rewritten when the code
    is changed when a step involves verifying a block of text.

    It is a time saver when you only want to make modifications to
    messages output by a program and ensure that those modifications
    are verified.

    Instead of manually constructing the exact output you are expecting
    you can simply visually inspect the output to verify that it is
    the desired output.

    This example shows a story being run in "rewrite" mode - where
    text strings are rewritten. This mode can be used when doing development
    when you expect textual changes.

    If the story passes then the file will be rewritten with the updated
    contents. If the story fails for any reason then the file will not
    be touched.

    If rewrite=False is fed through to the story engine instead, the story
    will always fail when seeing different text. This mode can be used when,
    for example, running all the stories on jenkins or when you are refactoring
    and *not* expecting textual output changes.
  given:
    example.story: |
      Do things:
        steps:
          - Do thing: x
          - Do thing: y
          - Do thing: z
          - Do other thing:
              variable 1: a
              variable 2: b

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

          def do_other_thing(self, variable_1=None, variable_2=None):
              if self._rewrite:
                  self.current_step.update(
                      variable_2="complicated:\nmultiline\nstring"
                  )
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathquery
      from engine import Engine
  variations:
    Rewritten:
      steps:
      - Run:
          code: |
            StoryCollection(pathquery(".").ext("story"), Engine(rewrite=True)).ordered_by_name().play()
          will output: |-
            RUNNING Do things in /path/to/example.story ... SUCCESS in 0.1 seconds.
            RUNNING Do things/Do more things in /path/to/example.story ... SUCCESS in 0.1 seconds.

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
                  variable 1: a
                  variable 2: |-
                    complicated:
                    multiline
                    string


              variations:
                Do more things:
                  steps:
                  - Do thing: |-
                      xxx:
                      yyy

    No changes:
      steps:
      - Run:
          code: |
            StoryCollection(pathquery(".").ext("story"), Engine(rewrite=False)).ordered_by_name().play()
          will output: |-
            RUNNING Do things in /path/to/example.story ... SUCCESS in 0.1 seconds.
            RUNNING Do things/Do more things in /path/to/example.story ... SUCCESS in 0.1 seconds.
      - Example story unchanged
