Generate documentation from stories:
  docs: generate-documentation
  status: experimental
  about: |
    hitchstory YAML stories are designed to be as readable as possible while
    still being terse and deduplicated. This means that the stories will not be
    as readable to people who do not have a deep understanding of the code.

    Where terseness and duplication trumps readability, the former
    take precedence. YAML stories are not intended to be a replacement for
    stakeholder documentation in and of themselves.

    YAML stories *are* designed, however, to be used to generate readable 
    documentation for use by stakeholders.

    The example shown below demonstrates how a story can be transformed into
    markdown via jinja2. This markdown can then be used to generate HTML
    with a static site generator.

    While markdown is the example given, in principle, any kind of text markup
    can be generated with the stories.
  given:
    core files:
      example.story: |
        Login:
          about: Simple log in.
          with:
            username: AzureDiamond
            password: hunter2
          given:
            url: /loginurl
          steps:
          - Fill form:
              username: (( username ))
              password: (( password ))
          - Click: login
          - Drag:
              from item: left
              to item: right


        Log in on another url:
          about: Alternate log in URL.
          based on: login
          given:
            url: /alternativeloginurl

        Log in as president:
          about: For stories that involve Trump.
          based on: login
          with:
            username: DonaldTrump
            password: iamsosmrt
      engine.py: |
        from hitchstory import BaseEngine, GivenDefinition, GivenProperty
        from strictyaml import Map, Int, Str, Optional


        class Engine(BaseEngine):
            given_definition = GivenDefinition(
                url=GivenProperty(schema=Str(), document="Load: {{ url }}"),
            )

            def set_up(self):
                print("visit {0}".format(self.given['url']))

            def fill_form(self, **textboxes):
                for name, text in sorted(textboxes.items()):
                    print("with {0}".format(name))
                    print("enter {0}".format(text))
              
            def drag(self, from_item, to_item):
                print(f"drag {from_item} to {to_item}")

            def click(self, item):
                print("clicked on {0}".format(item))

      index.jinja2: |
        {% for story in story_list %}
        {{ story.documentation }}
        {% endfor %}
      document.yaml: |
        story: |
          {{ story.name }}
          {{ "-" * story.name|length }}

          {{ story.about }}

          {% for name, property in story.given.items() %}
          {{ property.documentation }}
          {% endfor %}
          {% for step in story.steps %}
          {{ step.documentation }}
          {% endfor %}
        given:
          url: 'Load: {{ url }}'
        steps:
          fill form: |-
            {% for name, value in textboxes.items() %}
            - Enter text '{{ value }}' in {{ name }}.
            {%- endfor %}
          click: '* Click on {{ item }}'
          drag: '* Drag from {{ from_item }} to {{ to_item }}.'
    setup: |
      from hitchstory import StoryCollection
      from pathquery import pathquery
      from engine import Engine
      from path import Path
      from jinja2 import Template
  variations:
    Generate from story:
      steps:
      - run:
          code: |
            print(
                Template(Path("index.jinja2").text()).render(
                    story_list=StoryCollection(
                        pathquery(".").ext("story"), Engine()
                    ).non_variations().with_documentation(Path("document.yaml").text()).ordered_by_file()
                )
            )
          will output: |-
            Login
            -----

            Simple log in.


            Load: /loginurl



            - Enter text '(( username ))' in username.
            - Enter text '(( password ))' in password.

            * Click on login

            * Drag from left to right.


            Log in on another url
            ---------------------

            Alternate log in URL.


            Load: /alternativeloginurl



            - Enter text '(( username ))' in username.
            - Enter text '(( password ))' in password.

            * Click on login

            * Drag from left to right.


            Log in as president
            -------------------

            For stories that involve Trump.


            Load: /loginurl



            - Enter text '(( username ))' in username.
            - Enter text '(( password ))' in password.

            * Click on login

            * Drag from left to right.
