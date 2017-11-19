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
            story.play()
          raises:
            type: strictyaml.exceptions.YAMLValidationError
            message: |-
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
             def __init__(self):
                self.add_product = 1
      steps:
      - Run:
          code: |
            print(story.play().report())
          raises:
            type: hitchstory.exceptions.StepNotCallable
            message: |-
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
          code: story.play()
          raises:
            type: hitchstory.exceptions.StepNotFound
            message: Step with name 'add_product' not found in <engine.Engine object
              at 0xfffffffffff>.
    Mix of kwargs and regular arguments:
      given:
        engine.py: |
          from hitchstory import BaseEngine

          class Engine(BaseEngine):
              def add_product(self, name, **kwargs):
                  print('x')
      steps:
      - Run:
          code: story.play().report()
          raises:
            type: hitchstory.exceptions.CannotMixKeywordArgs
            message: Cannot mix keyword arguments (e.g. **kwargs) and regular args
              (e.g. x)

    Cannot use *args:
      given:
        engine.py: |
          from hitchstory import BaseEngine

          class Engine(BaseEngine):
              def add_product(self, *args):
                  pass
      steps:
      - Run:
          code: print(story.play().report())
          raises:
            type: hitchstory.exceptions.CannotUseVarargs
            message: Cannot use varargs (e.g. *args), can only use keyword args (**kwargs)

    Cannot use single argument:
      given:
        example.story: |
          Create files:
            steps:
              - Add product: Towel
        engine.py: |
          from hitchstory import BaseEngine

          class Engine(BaseEngine):
              def add_product(self, name, quantity):
                  pass
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.StepMethodNeedsMoreThanOneArgument
            message: Step method <bound method Engine.add_product of <engine.Engine
              object at 0xfffffffffff>> requires 2 arguments, got one.
