Exception in special methods:
  given:
    example.story: |
      Do thing:
        steps:
          - Do thing
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine


      story = StoryCollection(pathq(".").ext("story"), Engine()).one()
  variations:
    in on_success:
      given:
        engine.py: |
          from hitchstory import BaseEngine
          from code_that_does_things import raise_example_exception

          class Engine(BaseEngine):
              def do_thing(self):
                  pass

              def on_success(self):
                  raise_example_exception()
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.OnSuccessException
            message: "Stacktrace:\n\n[[ RED ]][[ BRIGHT ]]code_that_does_things.ExampleException[[\
              \ RESET ALL ]]\n  [[ DIM ]][[ RED ]]\n    This is a demonstration exception's\
              \ docstring.\n\n    It spreads across multiple lines.\n    [[ RESET\
              \ ALL ]]\n[[ RED ]][[ RESET FORE ]]"

    in on_failure:
      given:
        engine.py: |
          from hitchstory import BaseEngine
          from code_that_does_things import *

          class Engine(BaseEngine):
              def do_thing(self):
                  raise_example_exception()

              def on_failure(self, result):
                  raise_example_exception()
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.OnFailureException
            message: "Stacktrace:\n\n[[ RED ]][[ BRIGHT ]]code_that_does_things.ExampleException[[\
              \ RESET ALL ]]\n  [[ DIM ]][[ RED ]]\n    This is a demonstration exception's\
              \ docstring.\n\n    It spreads across multiple lines.\n    [[ RESET\
              \ ALL ]]\n[[ RED ]][[ RESET FORE ]]"

    in tear_down:
      given:
        engine.py: |
          from hitchstory import BaseEngine
          from code_that_does_things import *

          class Engine(BaseEngine):
              def do_thing(self):
                  pass

              def tear_down(self):
                  raise_example_exception()
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.TearDownException
            message: "Stacktrace:\n\n[[ RED ]][[ BRIGHT ]]code_that_does_things.ExampleException[[\
              \ RESET ALL ]]\n  [[ DIM ]][[ RED ]]\n    This is a demonstration exception's\
              \ docstring.\n\n    It spreads across multiple lines.\n    [[ RESET\
              \ ALL ]]\n[[ RED ]][[ RESET FORE ]]"
