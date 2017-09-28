Descriptive parameters attached to story:
  preconditions:
    example.story: |
      Build city:
        description: A great city. The best.
        jiras: JIRA-123, JIRA-124
        features: files, creating
        scenario:
          - Reticulate splines

      Live in city:
        jiras: JIRA-789
        features: other
        scenario:
          - Kick llama's ass
    setup: |
      from hitchstory import StoryCollection, BaseEngine, StorySchema
      from strictyaml import Map, Str, CommaSeparated, Optional
      from pathquery import pathq
      from code_that_does_things import *


      class Engine(BaseEngine):
          schema = StorySchema(
              about={
                  Optional("description"): Str(),
                  "jiras": CommaSeparated(Str()),
                  "features": CommaSeparated(Str()),
              },
          )

          def reticulate_splines(self):
              reticulate_splines()

          def kick_llamas_ass(self):
              kick_llamas_ass()
  variations:
    Run all stories:
      preconditions:
        code: |
          StoryCollection(pathq(".").ext("story"), Engine()).ordered_by_name().play()
      scenario:
      - Run code
      - Splines reticulated
      - Llama's ass kicked

    Run only filtered stories:
      preconditions:
        code: |
          StoryCollection(pathq(".").ext("story"), Engine()).filter(lambda story: "JIRA-124" in story.about['jiras']).ordered_by_name().play()
      scenario:
      - Run code
      - Splines reticulated

