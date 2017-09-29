Exception in special methods:
  preconditions:
    example.story: |
      Do thing:
        scenario:
          - Do thing
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine
    code: |
      StoryCollection(pathq(".").ext("story"), Engine()).one().play()
  variations:
    in on_success:
      preconditions:
        engine.py: |
          from hitchstory import BaseEngine
          from code_that_does_things import *

          class Engine(BaseEngine):
              def do_thing(self):
                  pass

              def on_success(self):
                  raise_example_exception()
      scenario:
      - Long form exception raised:
          artefact: exception in on_success


    in on_failure:
      preconditions:
        engine.py: |
          from hitchstory import BaseEngine
          from code_that_does_things import *

          class Engine(BaseEngine):
              def do_thing(self):
                  raise_example_exception()

              def on_failure(self, result):
                  raise_example_exception()
      scenario:
      - Long form exception raised:
          artefact: exception in on_failure


    in tear_down:
      preconditions:
        engine.py: |
          from hitchstory import BaseEngine
          from code_that_does_things import *

          class Engine(BaseEngine):
              def do_thing(self):
                  pass

              def tear_down(self):
                  raise_example_exception()
      scenario:
      - Long form exception raised:
          artefact: exception in tear_down
