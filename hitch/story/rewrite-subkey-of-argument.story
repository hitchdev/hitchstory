Story that rewrites the sub key of an argument:
  docs: engine/rewrite-subkey-of-argument
  about: |
    This shows how to build a story that rewrites a sub-key
    of an argument.

    ```
    self.current_step.rewrite("response", "content").to("new output")
    ```

  given:
    files:
      example.story: |
        REST API:
          steps:
          - API call:
              request:
                path: /hello
              response:
                status code: 200
                content: |
                  {"old": "response"}
      engine.py: |
        from hitchstory import BaseEngine

        class Engine(BaseEngine):
            def __init__(self, rewrite=True):
                self._rewrite = rewrite
            
            def run(self, command):
                pass

            def api_call(self, request, response):
                if self._rewrite:
                    self.current_step.rewrite(
                        "response", "content"
                    ).to("""{"new": "output"}""")

    setup: |
      from hitchstory import StoryCollection
      from pathlib import Path
      from engine import Engine
  variations:
    Story is rewritten when rewrite=True is used:
      steps:
      - Run:
          code: |
            StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).ordered_by_name().play()
          will output: |-
            RUNNING REST API in /path/to/working/example.story ... SUCCESS in 0.1 seconds.

      - File contents will be:
          filename: example.story
          contents: |-
            REST API:
              steps:
              - API call:
                  request:
                    path: /hello
                  response:
                    status code: 200
                    content: |-
                      {"new": "output"}

    Story remains unchanged when rewrite=False is used instead:
      steps:
      - Run:
          code: |
            StoryCollection(Path(".").glob("*.story"), Engine(rewrite=False)).ordered_by_name().play()
          will output: |-
            RUNNING REST API in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
      - Example story unchanged
