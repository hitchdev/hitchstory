All stories must have a unique name:
  description: |
    Note that "Create file" and "create file" are not exactly
    the same name, but their slugified names are identical.
  given:
    example1.story: |
      Create file:
        steps:
          - Create file
    example2.story: |
      create-file:
        steps:
           - Create file
    setup: |
      from hitchstory import StoryCollection, BaseEngine
      from pathquery import pathq

      class Engine(BaseEngine):
          def create_file(self, filename="step1.txt", content="example"):
              with open(filename, 'w') as handle:
                  handle.write(content)
  steps:
  - Run:
      code: |
        StoryCollection(pathq(".").ext("story"), Engine()).ordered_arbitrarily()
      raises:
        type: hitchstory.exceptions.DuplicateStoryNames
        message: Story 'Create file' in '/path/to/example1.story' and 'create-file'
          in '/path/to/example2.story' are identical when slugified ('create-file'
          and 'create-file').
