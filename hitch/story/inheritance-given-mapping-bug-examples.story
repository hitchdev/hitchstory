Story inheritance todos bug:
  given:
    files:
      example.story: |
        Parent:
          given:
            data:
              todos.todo:
                10:
                  title: Buy peppers
                  created_at: 2023-05-08T16:29:41.595Z
                  update_at: 2023-05-08T16:29:41.595Z
                  isCompleted: no
                11:
                  title: Buy cereal
                  created_at: 2023-05-08T16:29:41.595Z
                  update_at: 2023-05-08T16:29:41.595Z
                  isCompleted: yes

        Child:
          based on: parent
          given:
            data:
              todos.todo:
                # Also includes peppers and cereal
                12:
                  title: Buy a toaster
                  created_at: 2023-05-08T16:29:41.595Z
                  update_at: 2023-05-08T16:29:41.595Z
                  isCompleted: yes
          steps:
          - Load data

      engine.py: |
        from hitchstory import BaseEngine, GivenDefinition, GivenProperty
        from strictyaml import Map, Int, Str, MapPattern, Optional, Enum, Bool


        class Engine(BaseEngine):
            given_definition = GivenDefinition(
                data=GivenProperty(
                    schema=MapPattern(
                        Enum(["todos.todo"]),
                        MapPattern(
                            Int(),
                            Map(
                                {
                                    "title": Str(),
                                    "created_at": Str(),
                                    "update_at": Str(),
                                    "isCompleted": Bool(),
                                }
                            ),
                        ),
                    ),
                    inherit_via=GivenProperty.OVERRIDE,
                ),
            )

            def set_up(self):
                pass

            def load_data(self):
                for pk in self.given["data"]["todos.todo"].keys():
                    print(pk)
    setup: |
      from hitchstory import StoryCollection
      from engine import Engine
      from pathlib import Path

      collection = StoryCollection(Path(".").glob("*.story"), Engine())
  steps:
  - Run:
      code: collection.named("Child").play()
      will output: |-
        RUNNING Child in /path/to/working/example.story ... 10
        11
        12
        SUCCESS in 0.1 seconds.
