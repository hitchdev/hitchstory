Strong typing:
  description: |
    You can define the structure of the arguments
    fed to your steps using "validate" using StrictYAML
    validators.

    This will not only validate the data fed to your
    steps, it will convert it to the correct types
    as well.

    This feature is optional as all parameters will,
    by default, be parsed as strings, lists and dicts
    instead.
  given:
    example.story: |
      Create files:
        given:
          x: 1
        steps:
          - Add product:
              name: Towel
              versions:
                - 2.6
                - 2.3.4
              quantity: 2
              options:
                tagline: Hoopy
                nametag: Ford Prefect
          - Put back items: 1
    engine.py: |
      from hitchstory import BaseEngine, validate, GivenDefinition, GivenProperty, StorySchema
      from strictyaml import Seq, Str, Int, Map
      from code_that_does_things import append

      class Engine(BaseEngine):
          given_definition = GivenDefinition(
              x=GivenProperty(schema=Int()),
          )

          def set_up(self):
              pass

          @validate(
              versions=Seq(Str()),
              quantity=Int(),
              options=Map({
                  'tagline': Str(), 'nametag': Str()
              }),
          )
          def add_product(
              self,
              quantity,
              name=None,
              versions=None,
              options=None
          ):
              assert type(quantity) is int, "quantity is of type {0}".format(type(quantity))
              assert type(versions[0]) is str
              assert type(options['tagline']) is str
              append(options['nametag'])

          @validate(number_of_items=Int())
          def put_back_items(self, number_of_items):
              assert type(number_of_items) is int
              append("Items put back: " + str(number_of_items))

          def tear_down(self):
              pass
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine
  steps:
  - Run:
      code: |
        result = StoryCollection(pathq(".").ext("story"), Engine()).ordered_by_name().play()
        print(result.report())
  - Output is: |
      Ford Prefect
      Items put back: 1

