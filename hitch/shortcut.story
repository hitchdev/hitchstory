Shortcut lookup for story names:
  given:
    example1.story: |
      Create file:
        steps:
          - Create file
      Create file again:
        steps:
          - Create file
    example2.story: |
      Create files:
        steps:
          - Create file
    setup: |
      from hitchstory import StoryCollection, BaseEngine
      from pathquery import pathq

      class Engine(BaseEngine):
          def create_file(self, filename="step1.txt", content="example"):
              with open(filename, 'w') as handle:
                  handle.write(content)

      story_collection = StoryCollection(pathq(".").ext("story"), Engine())
  variations:
    Story not found:
      steps:
      - Run:
          code: story_collection.shortcut("toast").play()
          raises:
            type: hitchstory.exceptions.StoryNotFound
            message: Story 'toast' not found.

    More than one story found:
      steps:
      - Run:
          code: story_collection.shortcut("file").play()
          raises:
            type: hitchstory.exceptions.MoreThanOneStory
            message: "More than one matching story:\nCreate file (in /path/to/example1.story)\n\
              Create file again (in /path/to/example1.story)\nCreate files (in /path/to/example2.story)"

    Story found and run:
      steps:
      - Run:
          code: |
            results = story_collection.shortcut("file", "again").play()
            print(results.report())
          will output: 'STORY RAN SUCCESSFULLY /path/to/example1.story: Create file
            again in 0.1 seconds.'

