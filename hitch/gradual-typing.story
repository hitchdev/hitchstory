Gradual typing of story steps:
  docs: gradual-typing
  about: |
    In order to speed up prototyping and development
    of a story suite, the structure of your YAML data
    specified in preconditions, parameters and step
    arguments need not be specified in advance.

    All data that is parsed without a validator
    is parsed either as a dict, list or string, as
    per the StrictYAML spec.

    When your story suite matures and the structure of
    your story files has solidified, you can
    specify validators that fail fast when YAML
    snippets with an invalid structure are used.
  given:
    example.story: |
      Create files:
        given:
          files created:
            preconditionfile.txt:
              some text
        steps:
          - Create file:
              details:
                file name: step1.txt
                content: some other text
    engine.py: |
      from hitchstory import BaseEngine, GivenDefinition, GivenProperty


      class Engine(BaseEngine):
          given_definition = GivenDefinition(
              files_created=GivenProperty(),
          )
      
          def set_up(self):
              for filename, contents in self.given['files_created'].items():
                  with open(filename, 'w') as handle:
                      handle.write(contents)

          def create_file(self, details):
              with open(details['file name'], 'w') as handle:
                  handle.write(details['content'])
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathquery
      from engine import Engine
  steps:
  - Run:
      code: |
        StoryCollection(pathquery(".").ext("story"), Engine()).named("Create files").play()
      will output: RUNNING Create files in /path/to/example.story ... SUCCESS in 0.1
        seconds.
  - File was created with:
      filename: preconditionfile.txt
      contents: some text
  - File was created with:
      filename: step1.txt
      contents: some other text
