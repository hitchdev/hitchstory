Story that rewrites given preconditions:
  docs: engine/rewrite-given
  about: |
    These examples show how to build stories that rewrite themselves
    from program output (in-test snapshot testing) but that rewrite
    the given preconditions.

    This is useful for auto-updating given preconditions when, for
    example, a REST API service that is being mocked starts
    returning different data.

    ```
    self.current_step.rewrite("argument").to("new output")
    ```

  given:
    files:
      example.story: |
        Call API:
          given:
            mock api:
              request: |
                {"greeting": "hello"}
              response: |
                {"greeting": "hi"}
          steps:
            - Call API
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

  steps:
  - Run:
      code: |
        StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).ordered_by_name().play()
      will output: |-
        RUNNING Call API in /path/to/working/example.story ... SUCCESS in 0.1 seconds.

  - File contents will be:
      filename: example.story
      contents: |-
        Call API:
          given:
            mock api:
              request: |
                {"greeting": "hello"}
              response: |
                {"greeting": "bye"}
          steps:
          - Call API
