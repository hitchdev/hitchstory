Invalid story:
  given:
    example.story: |
      Create files:
        steps:
          - Add product:
              name: Towel
              quantity: Three
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathquery import pathq

      story = StoryCollection(pathq(".").ext("story"), Engine()).one()
  variations:
    Invalid type in step:
      given:
        engine.py: |
          from hitchstory import BaseEngine, validate
          from strictyaml import Int

          class Engine(BaseEngine):
              @validate(quantity=Int())
              def add_product(self, name, quantity):
                  pass
      steps:
      - Run:
          code: |
            print(story.play().report())
          will output: |-
            --> 107 :                 "when expecting an integer",
                    108 :             )



            [7]: function 'expecting_but_found'
              /home/colm/.hitch/90646u/py3.5.0/lib/python3.5/site-packages/strictyaml/yamllocation.py


                    21 :             expecting,
                    22 :             found if found is not None else "found {0}".format(self.found()),
                --> 23 :             self
                    24 :         )



            strictyaml.exceptions.YAMLValidationError
              None
            when expecting an integer
            found arbitrary text
              in "<unicode string>", line 5, column 1:
                      quantity: Three
                ^ (line: 5)

    Invalid validator on step:
      given:
        engine.py: |
          from hitchstory import BaseEngine, validate
          from strictyaml import Int

          class Engine(BaseEngine):
              @validate(not_an_argument=Int())
              def add_product(self, name, quantity):
                  pass
      steps:
      - Run:
          code: |
            print(story.play().report())
          raises:
            type: hitchstory.exceptions.StepContainsInvalidValidator
            message: Step <function Engine.add_product at 0xfffffffffff> does not
              contain argument 'not_an_argument' listed as a validator.

    Callable step not found:
      given:
        engine.py: |
          from hitchstory import BaseEngine

          class Engine(BaseEngine):
            def set_up(self):
                # add_product needs to be a method to be treated as a step
                self.add_product = 1

            def tear_down(self):
                pass
      steps:
      - Run:
          code: |
            print(story.play().report())
          will output: |-
            FAILURE IN /path/to/example.story:
                "Create files" in 0.1 seconds.


                Create files:
                  steps:
                  - Add product:
                      name: Towel
                      quantity: Three



            hitchstory.exceptions.StepNotCallable

                The step you tried to call is not a python method.

            Step with name 'add_product' in <engine.Engine object at 0xfffffffffff> is not a function or a callable object, it is a <class 'int'>
    Method not found:
      given:
        engine.py: |
          from hitchstory import BaseEngine

          class Engine(BaseEngine):
            def set_up(self):
                pass

            def tear_down(self):
                pass
      steps:
      - Run:
          code: print(story.play().report())
          will output: |-
            FAILURE IN /path/to/example.story:
                "Create files" in 0.1 seconds.


                Create files:
                  steps:
                  - Add product:
                      name: Towel
                      quantity: Three



            hitchstory.exceptions.StepNotFound

                Step in story has no corresponding method in engine.

            Step with name 'add_product' not found in <engine.Engine object at 0xfffffffffff>.
