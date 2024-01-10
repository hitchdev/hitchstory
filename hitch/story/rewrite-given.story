Story that rewrites given preconditions:
  docs: engine/rewrite-given
  about: |
    These examples show how to build stories that rewrite their given
    preconditions from program output.

    This is useful for auto-updating given preconditions when the
    outside world changes. For example, if a a REST API service that
    is being mocked starts returning different data you can
    run the story in rewrite mode to update the mock.

    The command to perform this rewrite is:

    ```
    self.current_step.rewrite("argument").to("new output")
    ```

    Note that if there is a story inheritance hierarchy then only the
    child story's given preconditions will be updated.

  given:
    files:
      example1.story: |
        Basic:
          given:
            mock api:
              request: |
                {"greeting": "hello"}
              response: |
                {"greeting": "hi"}
          steps:
            - Call API

      example2.story: |
        Overridden response:
          based on: basic
          given:
            mock api:
              response: |
                {"greeting": "bonjour"}

      example3.story: |
        Overridden request:
          based on: basic
          given:
            mock api:
              request: |
                {"greeting": "hi there"}
      engine.py: |
        from hitchstory import BaseEngine, GivenDefinition, GivenProperty
        from strictyaml import Map, Str

        class Engine(BaseEngine):
            given_definition = GivenDefinition(
                mock_api=GivenProperty(
                    schema=Map({"request": Str(), "response": Str()}),
                    inherit_via=GivenProperty.OVERRIDE,
                ),
            )

            def __init__(self, rewrite=True):
                self._rewrite = rewrite
            
            def call_api(self):
                if self._rewrite:
                    self.given.rewrite("Mock API", "response").to("""{"greeting": "bye"}\n""")

    setup: |
      from hitchstory import StoryCollection
      from pathlib import Path
      from engine import Engine

  variations:
    Simple:
      steps:
      - Run:
          code: |
            StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).named("Basic").play()
          will output: |-
            RUNNING Basic in /path/to/working/example1.story ... SUCCESS in 0.1 seconds.

      - File contents will be:
          filename: example1.story
          contents: |-
            Basic:
              given:
                mock api:
                  request: |
                    {"greeting": "hello"}
                  response: |
                    {"greeting": "bye"}
              steps:
              - Call API

    Overridden response:
      steps:
      - Run:
          code: |
            StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).named("Overridden response").play()
          will output: |-
            RUNNING Overridden response in /path/to/working/example2.story ... SUCCESS in 0.1 seconds.

      - File contents will be:
          filename: example2.story
          contents: |-
            Overridden response:
              based on: basic
              given:
                mock api:
                  response: |
                    {"greeting": "bye"}

    Overridden request:
      steps:
      - Run:
          code: |
            StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).named("Overridden request").play()
          will output: |-
            RUNNING Overridden request in /path/to/working/example3.story ... SUCCESS in 0.1 seconds.

      - File contents will be:
          filename: example3.story
          contents: |-
            Overridden request:
              based on: basic
              given:
                mock api:
                  request: |
                    {"greeting": "hi there"}
                  response: |
                    {"greeting": "bye"}

