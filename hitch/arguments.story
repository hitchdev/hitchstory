Steps with arbitrary numbers of named arguments:
  description: |
    When you need arbitrary numbers of arguments for
    a step, you can use **kwargs to feed them in.
  given:
    example.story: |
      Create files:
        steps:
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
      from hitchstory import StoryCollection
      from engine import Engine
      from pathquery import pathq
    code:
  steps:
  - Run:
      code: |
        result = StoryCollection(pathq(".").ext("story"), Engine()).named("Create files").play()
        print(result.report())
      will output: 'STORY RAN SUCCESSFULLY /path/to/example.story: Create files in
        0.1 seconds.'
  - File was created with:
      filename: Filename1.txt
      contents: example
  - File was created with:
      filename: File name with space.txt
      contents: example
