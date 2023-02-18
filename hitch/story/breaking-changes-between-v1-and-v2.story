Upgrading breaking changes between v1 and v2:
  about: |
    Version 2 contains two important but quite easy to fix breaking changes:

    * For every GivenProperty with a mapping schema inherit_via must be specified as either OVERRIDE or REPLACE.

    * TODO : steps -> replacement steps / follow on steps.
  given:
    core files:
      example.story: |
        Create files:
          given:
            x:
              a: a
              b: b
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
    GivenProperty with a mapping schema have inherit_via specified:
      about: |
        In this example, inherit_via is not specified on GivenProperty.
      given:
        files:
          engine.py: |
            from hitchstory import BaseEngine, GivenDefinition, GivenProperty, validate
            from strictyaml import Int, Map, Str

            class Engine(BaseEngine):
                given_definition = GivenDefinition(
                    browser=GivenProperty(
                        schema=Map({"type": Str(), "size": Str()}),
                    ),
                )

                @validate(quantity=Int())
                def add_product(self, name, quantity):
                    pass
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.InheritViaRequired
            message: inherit_via is required on every GivenProperty that has a strictyaml
              mapping schema (i.e. Map or MapPattern).


    GivenProperty without a mapping schema must not have inherit_via specified:
      about: |
        In this example, inherit_via is specified on a GivenProperty schema with an strictyaml Any schema specified. It would behave the same way if Seq(), Str()
        or Int() or any other scalar validator were used.
      given:
        files:
          engine.py: |
            from hitchstory import BaseEngine, GivenDefinition, GivenProperty, validate
            from strictyaml import Int, Map, Str, Any

            class Engine(BaseEngine):
                given_definition = GivenDefinition(
                    browser=GivenProperty(
                        schema=Any(),
                        inherit_via=GivenProperty.OVERRIDE,
                    ),
                )

                @validate(quantity=Int())
                def add_product(self, name, quantity):
                    pass
      steps:
      - Run:
          code: story.play()
          raises:
            type: hitchstory.exceptions.InheritViaDisallowed
            message: inherit_via cannot be used on non mapping-schemas (i.e. every
              schema that isn't Map or MapPattern).
