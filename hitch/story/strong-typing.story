Strong typing:
  docs: engine/strong-typing
  about: |
    Unlike some other integration testing frameworks, HitchStory
    can strictly validate all tests and fail before running
    them if they do not adhere to the schema.

    Without validators all step/given data will be parsed as
    dict, list and string [as seen here](../gradual-typing).

    In order to restrict what kind of YAML is allowed
    and/or to parse strings into a different type (e.g.
    integers), you can use the **validator** decorator
    on step methods and the **schema** parameter
    on the GivenProperty object.
    
    The validator decorator and schema parameters
    take all valid [StrictYAML validators](../../../../strictyaml/using).
  given:
    files:
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
            - Add generic product:
                name: Towel
                versions:
                  - 2.6
                  - 2.3.4
                quantity: 2
                options:
                  tagline: Hoopy
                  nametag: Ford Prefect
      engine.py: |
        from hitchstory import BaseEngine, validate, GivenDefinition, GivenProperty
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
              
          
            @validate(kwargs=Map({
                "name": Str(),
                "quantity": Int(),
                "versions": Seq(Str()),
                "options": Map({
                    'tagline': Str(), 'nametag': Str()
                })
            }))
            def add_generic_product(self, **kwargs):
                assert type(kwargs['quantity']) is int, "quantity is of type {0}".format(type(kwargs['quantity']))
                assert type(kwargs['versions'][0]) is str
                assert type(kwargs['options']['tagline']) is str

            def tear_down(self):
                pass
    setup: |
      from hitchstory import StoryCollection
      from pathlib import Path
      from engine import Engine
  steps:
  - Run:
      code: |
        StoryCollection(Path(".").glob("*.story"), Engine()).ordered_by_name().play()
      will output: |-
        RUNNING Create files in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
  - Output is: |
      Ford Prefect
      Items put back: 1

