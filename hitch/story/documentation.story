Generate documentation from stories:
  docs: generate-documentation
  based on: inherit one story from another
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
    files:
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


            Log in on another url
            ---------------------

            Alternate log in URL.


            Load: /alternativeloginurl



            - Enter text '(( username ))' in username.
            - Enter text '(( password ))' in password.

            * Click on login


            Log in as president
            -------------------

            For stories that involve Trump.


            Load: /loginurl



            - Enter text '(( username ))' in username.
            - Enter text '(( password ))' in password.

            * Click on login
