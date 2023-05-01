Running a single named story successfully:
  category: runner
  docs: run-single-named-story
  about: |
    How a story runs when it is successful - i.e. when no exception
    is raised during its run.
  given:
    files:
      example.story: |
        Create files:
          steps:
            - Create file
            - Create file: step2.txt
            - Create file:
                file name: step3.txt
                content: third step
      engine.py: |
        from hitchstory import BaseEngine


        class Engine(BaseEngine):
            def create_file(self, file_name="step1.txt", content="example"):
                with open(file_name, 'w') as handle:
                    handle.write(content)

            def on_success(self):
                print("splines reticulated")

                with open("ranstory.txt", 'w') as handle:
                    handle.write(self.story.name)
    setup: |
      from hitchstory import StoryCollection
      from pathlib import Path
      from engine import Engine
  steps:
  - Run:
      code: |
        StoryCollection(Path(".").glob("*.story"), Engine()).named("Create files").play()
      will output: |-
        RUNNING Create files in /path/to/working/example.story ... splines reticulated
        SUCCESS in 0.1 seconds.
  - File was created with:
      filename: step1.txt
      contents: example
  - File was created with:
      filename: step2.txt
      contents: example
  - File was created with:
      filename: step3.txt
      contents: third step
  - File was created with:
      filename: ranstory.txt
      contents: Create files
