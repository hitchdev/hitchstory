All stories must have a unique name:
  description: |
    Note that "Create file" and "create file" are not exactly
    the same name, but their slugified names are identical.
  preconditions:
    example1.story: |
      Create file:
        scenario:
          - Create file
    example2.story: |
      create-file:
        scenario:
           - Create file
    setup: |
      from hitchstory import StoryCollection, BaseEngine
      from pathquery import pathq

      class Engine(BaseEngine):
          def create_file(self, filename="step1.txt", content="example"):
              with open(filename, 'w') as handle:
                  handle.write(content)
    code: |
      StoryCollection(pathq(".").ext("story"), Engine())

  scenario:
  - Raises Exception: |
      Story 'Create file' in '/home/colm/.hitch/90646u/state/example1.story' and 'create-file' in '/home/colm/.hitch/90646u/state/example2.story' are identical when slugified ('create-file' and 'create-file').

