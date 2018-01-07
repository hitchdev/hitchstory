Documentation:
  based on: inherit one story from another
  #status: experimental
  #description: |
    #While hitchstory YAML stories are designed to be as
    #readable as possible while still remaining terse and easy to maintain,
    #they are not a complete replacement for user documentation.

    #However, using hitchstory you can use them as a template for generating
    #pretty, readable, flowing documentation for end users of your software,
    #managers, translators, maintainers and other stakeholders.

    #Below is an example of documentation generated using a set of jinja2
    #templates loaded from a dict (loaded from the documentation.templates YAML file).
  #given:
    #documentation.templates: |
      #story: |
        #{{ story.name }}
        #{{ "-" * story.name|length }}

        #{{ story.info['about'] }}

        #With:
        #{{ story.given['a'] }}

        #and
        #{{ story.given['b'] }}

        #{% for step in story.steps %}
        #{{ step.documentation() }}
        #{% endfor %}
      #do_thing_one: |
        #* Do thing one
      #do_thing_two: |
        #* Do thing two
      #do_thing_three: |
        #* Do thing three: {{ step['value'] }}
      #do_thing_four: |
        #* Do thing four: {% if 'x' in step %}{{ step['x'] }}{% endif %}, {{ step['y'] }}
    #setup: |
      #from hitchstory import StoryCollection
      #from pathquery import pathq
      #from engine import Engine
      #from path import Path
      #import strictyaml

      #collection = StoryCollection(pathq(".").ext("story"), Engine())\
          #.with_templates(
              #strictyaml.load(Path("documentation.templates").bytes().decode('utf8')).data
          #)
  #variations:
    #Generate from story:
      #steps:
      #- run:
          #code: print(collection.named("Write to file 1").documentation("story"))
          #will output: |-
            #Write to file 1
            #---------------



            #With:
            #1

            #and
            #2


            #* Do thing one

            #* Do thing three: 3

            #* Do thing four: 9, 10
