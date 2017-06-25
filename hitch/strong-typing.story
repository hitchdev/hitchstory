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
  preconditions:
    files:
      example.story: |
        Create files:
          scenario:
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
  scenario:
    - Run command: |
        from code_that_does_things import *
        from hitchstory import StoryCollection, BaseEngine, validate
        from strictyaml import Seq, Str, Int, Map
        from pathquery import pathq


        class Engine(BaseEngine):
            def set_up(self):
                pass

            @validate(
                versions=Seq(Str()),
                quantity=Int(),
                options=Map({"tagline": Str(), "nametag": Str()})
            )
            def add_product(self, quantity, name=None, versions=None, options=None):
                assert type(quantity) is int, "not an integer"
                assert type(versions[0]) is str, "not a string"
                output(options['nametag'])

            @validate(number_of_items=Int())
            def put_back_items(self, number_of_items):
                assert type(number_of_items) is int, "not an integer"
                append("Items put back: {0}".format(number_of_items))

            def tear_down(self):
                pass

        result = StoryCollection(pathq(".").ext("story"), Engine()).one().play()
        print(result.report())
    - Output is: |
        Ford Prefect
        Items put back: 1
