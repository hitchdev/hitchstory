Invalid story:
  preconditions:
    example.story: |
      Create files:
        scenario:
          - Add product:
              name: Towel
              quantity: Three
    setup: |
      from hitchstory import StoryCollection
      from code_that_does_things import *
      from engine import Engine
      from pathquery import pathq
    code: |
      result = StoryCollection(pathq(".").ext("story"), Engine()).one().play()
      output(result.report())

  variations:
    Invalid type in step:
      preconditions:
        engine.py: |
          from hitchstory import BaseEngine, validate
          from strictyaml import Int

          class Engine(BaseEngine):
              @validate(quantity=Int())
              def add_product(self, name, quantity):
                  pass
      scenario:
      - Run code
      - Output contains: found non-integer

    Invalid validator on step:
      preconditions:
        engine.py: |
          from hitchstory import BaseEngine, validate
          from strictyaml import Int

          class Engine(BaseEngine):
              @validate(not_an_argument=Int())
              def add_product(self, name, quantity):
                  pass
      scenario:
      - Raises exception:
          exception_type: hitchstory.exceptions.StepContainsInvalidValidator
          message: Step <function Engine.add_product at 0x7fd810e91598> does not contain
            argument 'not_an_argument' listed as a validator.

    Callable step not found:
      preconditions:
        engine.py: |
          from hitchstory import BaseEngine

          class Engine(BaseEngine):
            def set_up(self):
                # add_product needs to be a method to be treated as a step
                self.add_product = 1

            def tear_down(self):
                pass
      scenario:
      - Run code
      - Output contains: not a function or a callable object

    Method not found:
      preconditions:
        engine.py: |
          from hitchstory import BaseEngine

          class Engine(BaseEngine):
            def set_up(self):
                pass

            def tear_down(self):
                pass
      scenario:
      - Run code
      - Output contains: not found
