Multiple stories played:
  preconditions:
    files:
      example1.story: |
        Create file:
          scenario:
            - Create file
        Create file again:
          scenario:
            - Create file
      example2.story: |
        Create files:
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
        command: StoryCollection(pathq(".").ext("story"), Engine()).one()
        exception: Create file again

    - Run command: |
        results = StoryCollection(pathq(".").ext("story"), Engine()).ordered_by_name().play()
        output(results.report())
    - Output is: |
        STORY RAN SUCCESSFULLY ((( anything )))/example1.story: Create file in 0.1 seconds.
        STORY RAN SUCCESSFULLY ((( anything )))/example1.story: Create file again in 0.1 seconds.
        STORY RAN SUCCESSFULLY ((( anything )))/example2.story: Create files in 0.1 seconds.


Multiple stories played in a filename:
  preconditions:
    files:
      example1.story: |
        Create file:
          scenario:
            - Create file
        Create file again:
          scenario:
            - Create file
      example2.story: |
        Create files:
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

    - Run command: |
        results = StoryCollection(pathq(".").ext("story"), Engine()).in_filename("example1.story").ordered_by_name().play()
        output(results.report())
    - Output is: |
        STORY RAN SUCCESSFULLY ((( anything )))/example1.story: Create file in 0.1 seconds.
        STORY RAN SUCCESSFULLY ((( anything )))/example1.story: Create file again in 0.1 seconds.
