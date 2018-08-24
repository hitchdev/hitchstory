Given preconditions:
  about: |
    All stories start with a set of preconditions. Hitchstory
    lets you define these 'given' preconditions using YAML
    and access them in the story using 'self.given['property name'].

    The underscoreified_names and precise StrictYAML schema
    must be defined using GivenDefinition and GivenProperty
    objects as shown below.
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
              output(self.given['thing'].get('content'))
              output(", ".join(self.given['List of things']))
              output(self.given['scalar thing'])
              output(sorted(self.given.keys()))
              #output(self.given.values())
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
            ['list_of_things', 'scalar_thing', 'thing']
            [('list_of_things', ['thing one', 'thing two']), ('scalar_thing', 35), ('thing', OrderedDict([('content', 'things')]))]

    Defaults:
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
            ['list_of_things', 'scalar_thing', 'thing']
            [('list_of_things', []), ('scalar_thing', None), ('thing', OrderedDict())]
