Exception in special methods:
  about: |
    The hitchstory engine has four 'special' methods -
    set_up, on_success, on_failure, and tear_down all
    of which can be overridden.
    
    set_up always runs at the beginning, tear_down at
    the end.
    
    on_success and on_failure run just before tear_down
    in the event of a successful or failed story run.

    If there is an exception in on_success, on_failure
    or tear_down, a corresponding exception is raised
    halting *all* stories from that point onward.

    Only exceptions in set_up or steps are considered
    normal.
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
          from code_that_does_things import *

          class Engine(BaseEngine):
              def do_thing(self):
                  pass

              def on_success(self):
                  raise_example_exception()

              def tear_down(self):
                  tear_down_was_run()
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.OnSuccessException
            message: "Stacktrace:\n\n[1]: function '[[ BRIGHT ]]on_success[[ RESET\
              \ ALL ]]'\n  /path/to/engine.py\n\n\n        6 :\n        7 :     def\
              \ on_success(self):\n    --> [[ BRIGHT ]]8[[ RESET ALL ]] :        \
              \ raise_example_exception()\n        9 :\n\n\n\n[2]: function '[[ BRIGHT\
              \ ]]raise_example_exception[[ RESET ALL ]]'\n  /path/to/code_that_does_things.py\n\
              \n\n        20 :\n        21 : def raise_example_exception(text=\"\"\
              ):\n    --> [[ BRIGHT ]]22[[ RESET ALL ]] :     raise ExampleException(text)\n\
              \        23 :\n\n\n\n[[ RED ]][[ BRIGHT ]]code_that_does_things.ExampleException[[\
              \ RESET ALL ]]\n  [[ DIM ]][[ RED ]]\n    This is a demonstration exception\
              \ docstring.\n\n    It spreads across multiple lines.\n    [[ RESET\
              \ ALL ]]\n[[ RED ]][[ RESET FORE ]]"
      - Tear down was run

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

              def tear_down(self):
                  tear_down_was_run()
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.OnFailureException
            message: "Stacktrace:\n\n[1]: function '[[ BRIGHT ]]on_failure[[ RESET\
              \ ALL ]]'\n  /path/to/engine.py\n\n\n        6 :\n        7 :     def\
              \ on_failure(self, result):\n    --> [[ BRIGHT ]]8[[ RESET ALL ]] :\
              \         raise_example_exception()\n        9 :\n\n\n\n[2]: function\
              \ '[[ BRIGHT ]]raise_example_exception[[ RESET ALL ]]'\n  /path/to/code_that_does_things.py\n\
              \n\n        20 :\n        21 : def raise_example_exception(text=\"\"\
              ):\n    --> [[ BRIGHT ]]22[[ RESET ALL ]] :     raise ExampleException(text)\n\
              \        23 :\n\n\n\n[[ RED ]][[ BRIGHT ]]code_that_does_things.ExampleException[[\
              \ RESET ALL ]]\n  [[ DIM ]][[ RED ]]\n    This is a demonstration exception\
              \ docstring.\n\n    It spreads across multiple lines.\n    [[ RESET\
              \ ALL ]]\n[[ RED ]][[ RESET FORE ]]"
      - Tear down was run

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
            message: "Stacktrace:\n\n[1]: function '[[ BRIGHT ]]tear_down[[ RESET\
              \ ALL ]]'\n  /path/to/engine.py\n\n\n        6 :\n        7 :     def\
              \ tear_down(self):\n    --> [[ BRIGHT ]]8[[ RESET ALL ]] :         raise_example_exception()\n\
              \        9 :\n\n\n\n[2]: function '[[ BRIGHT ]]raise_example_exception[[\
              \ RESET ALL ]]'\n  /path/to/code_that_does_things.py\n\n\n        20\
              \ :\n        21 : def raise_example_exception(text=\"\"):\n    --> [[\
              \ BRIGHT ]]22[[ RESET ALL ]] :     raise ExampleException(text)\n  \
              \      23 :\n\n\n\n[[ RED ]][[ BRIGHT ]]code_that_does_things.ExampleException[[\
              \ RESET ALL ]]\n  [[ DIM ]][[ RED ]]\n    This is a demonstration exception\
              \ docstring.\n\n    It spreads across multiple lines.\n    [[ RESET\
              \ ALL ]]\n[[ RED ]][[ RESET FORE ]]"
