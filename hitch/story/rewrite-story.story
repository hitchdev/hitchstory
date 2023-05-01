Story that rewrites itself:
  category: engine
  docs: rewrite-story
  about: |
    Unlike every other integration testing framework, Hitch stories
    are designed to be rewritten according to the detected output of
    a program.

    This lets you do rewrite acceptance test driven development (RATDD)
    - where you change the code, autoregenerate the story and visually
    inspect the new story to ensure it is correct.

    This example shows a story being run in "rewrite" mode (where
    rewrite=True) is fed to the engine and in normal mode.
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
                    will output: 
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
    Rewritten:
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

    No changes:
      steps:
      - Run:
          code: |
            StoryCollection(Path(".").glob("*.story"), Engine(rewrite=False)).ordered_by_name().play()
          will output: |-
            RUNNING Append text to file in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
            RUNNING Append text to file/Output text to in /path/to/working/example.story ... SUCCESS in 0.1 seconds.
      - Example story unchanged
