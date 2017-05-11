Strong typing:
  description: |
    You can define the structure of the arguments
    fed to your steps using "validate" using StrictYAML
    validators.

    This will not only validate the data fed to your
    steps, it will convert it to the correct types
    as well.
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
  scenario:
    - Run command: |
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
            def add_product(self, name=None, versions=None, quantity=None, options=None):
                assert type(versions[0]) is str, "not a string"
                assert type(quantity) is int, "not an integer"
                output(options['nametag'])

            def tear_down(self):
                pass

        result = StoryCollection(pathq(".").ext("story"), Engine()).one().play()
        print(result.report())
    - Output is: Ford Prefect
