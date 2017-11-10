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
            quantity: Three



            [3]: function 'validate_args'
              /home/colm/.hitch/90646u/py3.5.0/lib/python3.5/site-packages/hitchstory/arguments.py


                    41 :         Validate step using StrictYAML validators specified in @validate decorators.
                    42 :         """
                --> 43 :         self.yaml.revalidate(Map(validator, key_validator=UnderscoreCase()))
                    44 :         self.data = {}



            [4]: function 'revalidate'
              /home/colm/.hitch/90646u/py3.5.0/lib/python3.5/site-packages/strictyaml/representation.py


                    63 :             self._value = schema(self._chunk)._value
                    64 :         else:
                --> 65 :             schema(self._chunk)
                    66 :



            [5]: function '__call__'
              /home/colm/.hitch/90646u/py3.5.0/lib/python3.5/site-packages/strictyaml/validators.py


                    11 :
                    12 :     def __call__(self, chunk):
                --> 13 :         self.validate(chunk)
                    14 :         return YAML(



            [6]: function 'validate'
              /home/colm/.hitch/90646u/py3.5.0/lib/python3.5/site-packages/strictyaml/compound.py


                    93 :                 )
                    94 :
                --> 95 :             value.process(self._validator_dict[yaml_key.scalar](value))
                    96 :             key.process(yaml_key)



            [7]: function '__call__'
              /home/colm/.hitch/90646u/py3.5.0/lib/python3.5/site-packages/strictyaml/validators.py


                    34 :             return self._validator_a(chunk)
                    35 :         except YAMLValidationError as error:
                --> 36 :             return self._validator_b(chunk)
                    37 :



            [8]: function '__call__'
              /home/colm/.hitch/90646u/py3.5.0/lib/python3.5/site-packages/strictyaml/scalar.py


                    20 :         chunk.expect_scalar(self.rule_description)
                    21 :         return YAML(
                --> 22 :             self.validate_scalar(chunk),
                    23 :             text=chunk.contents,



            [9]: function 'validate_scalar'
              /home/colm/.hitch/90646u/py3.5.0/lib/python3.5/site-packages/strictyaml/scalar.py


                    105 :         if not utils.is_integer(val):
                    106 :             chunk.expecting_but_found(
                --> 107 :                 "when expecting an integer",
                    108 :             )



            [10]: function 'expecting_but_found'
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


    Mix of kwargs and regular arguments:
      given:
        engine.py: |
          from hitchstory import BaseEngine

          class Engine(BaseEngine):
              def add_product(self, name, **kwargs):
                  print('x')
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



            hitchstory.exceptions.CannotMixKeywordArgs

                **kwargs and regular args cannot be mixed in story step methods.

            Cannot mix keyword arguments (e.g. **kwargs) and regular args (e.g. x)

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
          will output: |-
            FAILURE IN /path/to/example.story:
                "Create files" in 0.1 seconds.


                Create files:
                  steps:
                  - Add product:
                      name: Towel
                      quantity: Three



            hitchstory.exceptions.CannotUseVarargs

                *args is not usable in step method.

            Cannot use varargs (e.g. *args), can only use keyword args (**kwargs)

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
          code: print(story.play().report())
          will output: |-
            FAILURE IN /path/to/example.story:
                "Create files" in 0.1 seconds.


                Create files:
                  steps:
                  - Add product: Towel



            hitchstory.exceptions.StepMethodNeedsMoreThanOneArgument

                Method in story engine takes more than one argument.

            Step method <bound method Engine.add_product of <engine.Engine object at 0xfffffffffff>> requires 2 arguments, got one.
