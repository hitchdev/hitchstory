Documentation:
  based on: shortcut lookup for story names
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
        variations:
          A:
            steps:
            - Create file
          B:
            steps:
            - Create file

  variations:
    Non-variations:
      steps:
      - Run:
          code: |
            Ensure([
                story.name for story in story_collection.non_variations().ordered_by_name()
            ]).equals(
                ["Create file", "Create file again", "Create files", ]
            )
