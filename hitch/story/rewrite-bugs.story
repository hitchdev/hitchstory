Rewrite story with replacement steps bug:
  based on: Story that rewrites itself
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
              replacement steps:
              - Run and get output:
                  command: cat mytext.txt
                  will output: 
  steps:
  - Run:
      code: |
        StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True))\
          .named("Append text to file/Output text to").play()
      will output: |-
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
              replacement steps:
              - Run and get output:
                  command: cat mytext.txt
                  will output: |-
                    hello
                    hello

                    
Rewrite single argument incorrect:
  based on: Story that rewrites itself
  given:
    files:
      example.story: |
        Append text to file:
          steps:
          - Run: echo hello >> mytext.txt
          
      engine.py: |
        from hitchstory import BaseEngine

        class Engine(BaseEngine):
            def __init__(self, rewrite=True):
                self._rewrite = rewrite
            
            def run(self, command, will_output=None):
                if self._rewrite:
                    self.current_step.rewrite("will_output").to("hello\nhello")
    setup: |
      from hitchstory import StoryCollection
      from pathlib import Path
      from engine import Engine
  steps:
  - Run:
      code: |
        StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True))\
          .named("Append text to file").play()
      will output: |-
        RUNNING Append text to file in /path/to/working/example.story ... FAILED in 0.1 seconds.

            Append text to file:
              steps:
              - Run: echo hello >> mytext.txt



        [1]: function 'run'
          /path/to/working/engine.py


                6 :     def run(self, command, will_output=None):
                7 :         if self._rewrite:
            --> 8 :             self.current_step.rewrite("will_output").to("hello\nhello")
                9 :



        [2]: function 'to'
          /src/hitchstory/story_file.py


                66 :                     step_to_update[self._step.name] = text
                67 :                 else:
            --> 68 :                     raise exceptions.RewriteFailure(
                69 :                         f"'{key_to_update}' doesn't exist, only '{single_argument_name}' exists."



        hitchstory.exceptions.RewriteFailure

            An error occurred when trying to rewrite a story.

        'will_output' doesn't exist, only 'command' exists.
