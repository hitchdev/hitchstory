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
    example.story: |
      Create files:
        preconditions:
          x: 1
        default:
          var: 1
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
    engine.py: "from hitchstory import BaseEngine, validate, StorySchema\nfrom strictyaml\
      \ import Seq, Str, Int, Map\nfrom code_that_does_things import *\n  \nclass\
      \ Engine(BaseEngine):\n    schema = StorySchema(\n        preconditions={\"\
      x\": Int()},\n    )\n    def set_up(self):\n        pass\n\n    @validate(\n\
      \        versions=Seq(Str()),\n        quantity=Int(),\n        options=Map({\"\
      tagline\": Str(), \"nametag\": Str()}),\n    )\n    def add_product(self, quantity,\
      \ name=None, versions=None, options=None):\n        assert type(quantity) is\
      \ int, \"not an integer\"\n        assert type(versions[0]) is str, \"not a\
      \ string\"\n        assert type(options['tagline']) is str, \"not a string\"\
      \n        append(options['nametag'])\n\n    @validate(number_of_items=Int())\n\
      \    def put_back_items(self, number_of_items):\n        assert type(number_of_items)\
      \ is int, \"not an integer\"\n        append(\"Items put back: {}\".format(number_of_items))\n\
      \n    def tear_down(self):\n        pass\n"
    setup: |
      from hitchstory import StoryCollection
      from code_that_does_things import *
      from pathquery import pathq
      from engine import Engine
    code: |
      result = StoryCollection(pathq(".").ext("story"), Engine()).ordered_by_name().play()
      print(result.report())
  scenario:
  - Run code
  - Output is: |
      Ford Prefect
      Items put back: 1

