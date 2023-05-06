Story that rewrites itself:
  docs: engine/rewrite-story
  about: |
    These examples show how to build stories that rewrite themselves
    from program output (in-test snapshot testing). This can be done
    with 
    
    ```
    self.current_step.rewrite("argument").to("new output")
    ```
    
  given:
    files:
      example.story: |
        Append text to file:
          steps:
            - Run: echo hello >> mytext.txt
            - Run: echo hello >> mytext.txt
            - Run: echo hello >> mytext.txt

          variations:
            Output text to:
              following steps:
                - Run and get output:
                    command: cat mytext.txt
                    will output: old value
      engine.py: |
        from hitchstory import BaseEngine

        class Engine(BaseEngine):
            def __init__(self, rewrite=True):
                self._rewrite = rewrite
            
            def run(self, command):
                pass

            def run_and_get_output(self, command, will_output):
                if self._rewrite:
                    self.current_step.rewrite("will_output").to("hello\nhello")

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
            RUNNING Append text to file in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
            RUNNING Append text to file/Output text to in /path/to/working/example.story ... SUCCESS in 0.1 seconds.

      - File contents will be:
          filename: example.story
          contents: |-
            Append text to file:
              steps:
              - Run: echo hello >> mytext.txt
              - Run: echo hello >> mytext.txt
              - Run: echo hello >> mytext.txt

              variations:
                Output text to:
                  following steps:
                  - Run and get output:
                      command: cat mytext.txt
                      will output: |-
                        hello
                        hello

    Story remains unchanged when rewrite=False is used instead:
      steps:
      - Run:
          code: |
            StoryCollection(Path(".").glob("*.story"), Engine(rewrite=False)).ordered_by_name().play()
          will output: |-
            RUNNING Append text to file in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
            RUNNING Append text to file/Output text to in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
      - Example story unchanged
