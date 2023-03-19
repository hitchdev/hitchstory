Upgrade breaking changes between v0.14 and v0.15:
  docs: breaking-changes-between-v014-and-v015
  about: |  
    Version 0.15 contains two important breaking changes:

    * For every GivenProperty with a mapping schema inherit_via must be specified as either OVERRIDE or REPLACE.

    * If parent stories have steps, child stories must specify either "replacement steps" or "following steps" instead of "steps".
  given:
    core files:
      example.story: |
        Create files:
          given:
            browser:
              type: chrome
              size: 1024x768
          steps:
           - Add product:
              name: Towel
              quantity: 3
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathlib import Path

      collection = StoryCollection(Path(".").glob("*.story"), Engine())

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
          code: collection.one().play()
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
          code: collection.one().play()
          raises:
            type: hitchstory.exceptions.InheritViaDisallowed
            message: inherit_via cannot be used on non mapping-schemas (i.e. every
              schema that isn't Map or MapPattern).


    Using steps on child story where parent also has steps:
      about: |
        In this example a parent story has steps and a child story
        also has steps. Since this is ambiguous, this behavior
        is disallowed since version 2.0.

      given:
        files:
          example_child.story: |
            Create other files:
              based on: create files
              steps:
              - Add product:
                  name: Towel
                  quantity: 3
          engine.py: |
            from hitchstory import BaseEngine, GivenDefinition, GivenProperty, validate
            from strictyaml import Int, Map, Str

            class Engine(BaseEngine):
                given_definition = GivenDefinition(
                    browser=GivenProperty(
                        schema=Map({"type": Str(), "size": Str()}),
                        inherit_via=GivenProperty.OVERRIDE,
                    ),
                )

                @validate(quantity=Int())
                def add_product(self, name, quantity):
                    pass
      steps:
      - Run:
          code: collection.named("Create other files").play()
          raises:
            type: hitchstory.exceptions.AmbiguousSteps
            message: Since 'Create files' has steps, 'Create other files' must have
              either 'replacement steps' or 'following steps'
