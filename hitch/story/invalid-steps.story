Invalid story:
  given:
    files:
      example.story: |
        Create files:
          steps:
            - Add product:
                name: Towel
                quantity: Three
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathlib import Path

      story = StoryCollection(Path(".").glob("*.story"), Engine()).one()

  variations:
    Invalid YAML in step arguments:
      given:
        files:
          engine.py: |
            from hitchstory import BaseEngine, validate
            from strictyaml import Int

            class Engine(BaseEngine):
                @validate(quantity=Int())
                def add_product(self, name, quantity):
                    pass
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.InvalidStepYAML
            message: |-
              YAML Error in '/path/to/working/example.story' in file '/path/to/working/example.story':
              when expecting an integer
              found arbitrary text
                in "<unicode string>", line 5, column 1:
                        quantity: Three
                  ^ (line: 5)
    Invalid validator on step:
      given:
        files:
          engine.py: |
            from hitchstory import BaseEngine, validate
            from strictyaml import Int

            class Engine(BaseEngine):
                @validate(not_an_argument=Int())
                def add_product(self, name, quantity):
                    pass
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.StepContainsInvalidValidator
            message: Step <function Engine.add_product at 0xfffffffffff> does not
              contain argument 'not_an_argument' listed as a validator.

    Step method not callable:
      given:
        files:
          engine.py: |
            from hitchstory import BaseEngine

            class Engine(BaseEngine):
              def __init__(self):
                  self.add_product = 1
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.StepNotCallable
            message: |-
              Step with name 'add_product' in <engine.Engine object at 0xfffffffffff> is not a function or a callable object, it is a <class 'int'>

    Method not found:
      given:
        files:
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
            message: Step 'add_product' used in story 'Create files' in filename '/path/to/working/example.story'
              not found in <engine.Engine object at 0xfffffffffff>.
    Mix of kwargs and regular arguments:
      given:
        files:
          engine.py: |
            from hitchstory import BaseEngine

            class Engine(BaseEngine):
                def add_product(self, name, **kwargs):
                    print('x')
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.CannotMixKeywordArgs
            message: Method '<bound method Engine.add_product of <engine.Engine object
              at 0xfffffffffff>>' mixes keyword (e.g. *kwargs), and regular args (e.g.
              arg1, arg2, arg3). Mixing is not allowed
    Cannot use *args:
      given:
        files:
          engine.py: |
            from hitchstory import BaseEngine

            class Engine(BaseEngine):
                def add_product(self, *args):
                    pass
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.CannotUseVarargs
            message: Method '<bound method Engine.add_product of <engine.Engine object
              at 0xfffffffffff>>' uses varargs (e.g. *args), only keyword args (e.g.
              **kwargs) are valid

    Cannot use single argument:
      given:
        files:
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

    Found argument when there should be none:
      given:
        files:
          example.story: |
            Create files:
              steps:
                - Add product:
          engine.py: |
            from hitchstory import BaseEngine

            class Engine(BaseEngine):
                def add_product(self):
                    pass
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.StepShouldNotHaveArguments
            message: 'Step method <bound method Engine.add_product of <engine.Engine
              object at 0xfffffffffff>> cannot have one or more arguments, but it
              has at least one (maybe because of a : the end of the line).'

    Access key on self.given that does not exist:
      given:
        files:
          example.story: |
            Create files:
              steps:
                - Add product
          engine.py: |
            from hitchstory import BaseEngine

            class Engine(BaseEngine):
                def set_up(self):
                    print(self.given['nonexistent key'])

                def add_product(self):
                    pass
      steps:
      - Run:
          code: story.play()
          will output: |-
            RUNNING Create files in /path/to/working/example.story ... FAILED in 0.1 seconds.



            [1]: function 'set_up'
              /path/to/working/engine.py


                    2 : class Engine(BaseEngine):
                    3 :     def set_up(self):
                --> 4 :         print(self.given['nonexistent key'])
                    5 :



            [2]: function '__getitem__'
              /src/hitchstory/given.py


                    55 :             return self._preconditions[slug]
                    56 :         else:
                --> 57 :             raise KeyError(
                    58 :                 (



            builtins.KeyError
              Mapping key not found.
            "'nonexistent key' / 'nonexistent_key' not found from given. Preconditions available: None"
