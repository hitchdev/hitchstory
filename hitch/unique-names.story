All stories must have a unique name:
  preconditions:
    files:
      example1.story: |
        Create file:
          scenario:
            - Create file
      example2.story: |
        Create file:
          scenario:
            - Create file
  scenario:
    - Run command: |
        from hitchstory import StoryCollection, BaseEngine
        from pathquery import pathq


        class Engine(BaseEngine):
            def create_file(self, filename="step1.txt", content="example"):
                with open(filename, 'w') as handle:
                    handle.write(content)

    - Assert exception:
        command: StoryCollection(pathq(".").ext("story"), Engine())
        exception: DuplicateStoryNames

All stories must have a unique slugified name:
  preconditions:
    files:
      example1.story: |
        Create file:
          scenario:
            - Create file
      example2.story: |
        create file:
          scenario:
            - Create file
  scenario:
    - Run command: |
        from hitchstory import StoryCollection, BaseEngine
        from pathquery import pathq


        class Engine(BaseEngine):
            def create_file(self, filename="step1.txt", content="example"):
                with open(filename, 'w') as handle:
                    handle.write(content)

    - Assert exception:
        command: StoryCollection(pathq(".").ext("story"), Engine())
        exception: DuplicateStoryNames

