Gradual typing of story steps:
  description: |
    In order to speed up prototyping and development
    of a test suite, the structure of your YAML data
    specified in preconditions, parameters and step
    arguments need not be specified in advance.

    All data that is parsed without a validator
    is parsed either as a dict, list or string, as
    per the StrictYAML spec.

    When your test suite matures and the structure of
    your story files is more locked down, you can
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
      from hitchstory import BaseEngine


      class Engine(BaseEngine):
          def set_up(self):
              for filename, contents in self.given['files created'].items():
                  with open(filename, 'w') as handle:
                      handle.write(contents)

          def create_file(self, details):
              with open(details['file name'], 'w') as handle:
                  handle.write(details['content'])
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathq
      from engine import Engine
  steps:
  - Run:
      code: |
        result = StoryCollection(pathq(".").ext("story"), Engine()).named("Create files").play()
        print(result.report())
      will output: 'STORY RAN SUCCESSFULLY /path/to/example.story: Create files in
        0.1 seconds.'
  - File was created with:
      filename: preconditionfile.txt
      contents: some text
  - File was created with:
      filename: step1.txt
      contents: some other text
