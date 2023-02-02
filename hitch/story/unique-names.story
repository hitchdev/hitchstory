All stories must have a unique name:
  about: |
    Note that "Create file" and "create file" are not exactly
    the same name, but their slugified names are identical.
  given:
    files:
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
      from pathlib import Path

      class Engine(BaseEngine):
          def create_file(self, filename="step1.txt", content="example"):
              with open(filename, 'w') as handle:
                  handle.write(content)
  steps:
  - Run:
      code: |
        StoryCollection(Path(".").glob("*.story"), Engine()).ordered_by_file().play()
      raises:
        type: hitchstory.exceptions.DuplicateStoryNames
        message: Story 'Create file' in '/path/to/working/example1.story' and 'create-file'
          in '/path/to/working/example2.story' are identical when slugified ('create-file'
          and 'create-file').
