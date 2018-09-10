Given preconditions:
  docs: given
  about: |
    Stories optionally start with a set of preconditions.

    Hitchstory lets you define these 'given' preconditions using YAML
    mapping and access them in the story by using self.given as you
    would a dict - e.g. self.given['property name'].

    The given property names need to first be specified in the engine
    using GivenDefinition and GivenPropery - optionally
    with a [StrictYAML schema](https://hitchdev.com/strictyaml).
  given:
    example.story: |
      Create files:
        given:
          thing:
            content: things
          List of things:
          - thing one
          - thing two
          scalar thing: 35
        steps:
          - Create file
    engine.py: |
      from hitchstory import BaseEngine, GivenDefinition, GivenProperty
      from strictyaml import Str, Map, Seq, Int, MapPattern

      def output(contents):
          with open("output.txt", 'a') as handle:
              handle.write("{0}\n".format(contents))

      class Engine(BaseEngine):
          given_definition=GivenDefinition(
              thing=GivenProperty(schema=MapPattern(Str(), Str())),
              list_of_things=GivenProperty(schema=Seq(Str())),
              scalar_thing=GivenProperty(Int())
          )

          def create_file(self):
              output(self.given['thing'].get('content') if 'thing' in self.given else None)
              output(", ".join(self.given.get('List of things', [])))
              output(self.given['scalar thing'] if 'scalar thing' in self.given else None)
              output(self.given.get('scalar thing', 'default'))
              output(sorted(self.given.keys()))
              output(sorted(self.given.items()))
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathquery
      from engine import Engine
  variations:
    Specified:
      steps:
      - Run:
          code: |
            StoryCollection(pathquery(".").ext("story"), Engine()).one().play()
          will output: |-
            RUNNING Create files in /path/to/example.story ... SUCCESS in 0.1 seconds.
      - File contents will be:
          filename: output.txt
          contents: |-
            things
            thing one, thing two
            35
            35
            ['list_of_things', 'scalar_thing', 'thing']
            [('list_of_things', ['thing one', 'thing two']), ('scalar_thing', 35), ('thing', OrderedDict([('content', 'things')]))]

    Defaulting to empty list, None or empty dict:
      given:
        example.story: |
          Create files:
            steps:
              - Create file
      steps:
      - Run:
          code: |
            StoryCollection(pathquery(".").ext("story"), Engine()).one().play()
          will output: |-
            RUNNING Create files in /path/to/example.story ... SUCCESS in 0.1 seconds.
      - File contents will be:
          filename: output.txt
          contents: |-
            None

            None
            default
            []
            []
