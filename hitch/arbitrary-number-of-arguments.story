Steps with arbitrary numbers of named arguments:
  description: |
    When you need arbitrary numbers of arguments for
    a step, you can use **kwargs to feed them in.
  preconditions:
      example.story: |
        Create files:
          scenario:
            - Create files:
                Filename1.txt: example
                File name with space.txt: example
      engine.py: |
        from hitchstory import BaseEngine

        class Engine(BaseEngine):
            def create_files(self, **kwargs):
                for filename, content in kwargs.items():
                    with open(filename, 'w') as handle:
                        handle.write(content)
      setup: |
        from code_that_does_things import *
        from hitchstory import StoryCollection
        from engine import Engine
        from pathquery import pathq
      code: |
        result = StoryCollection(pathq(".").ext("story"), Engine()).named("Create files").play()
        output(result.report())
  scenario:
    - Run code
    - Output is: |
        STORY RAN SUCCESSFULLY ((( anything )))/example.story: Create files in 0.1 seconds.
    - File was created with:
        filename: Filename1.txt
        contents: example
    - File was created with:
        filename: File name with space.txt
        contents: example
