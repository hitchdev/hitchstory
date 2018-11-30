Generate documentation from stories:
  docs: generate-documentation
  based on: inherit one story from another
  status: experimental
  about: |
    While hitchstory YAML stories are designed to be as
    readable as possible while still remaining terse and easy to maintain,
    it is not readable user documentation and is not intended for use by
    stakeholders to understand how a system operates.

    However, stakeholders do *need* documentation and user stories form an
    excellent base to build documentation from.

    Using hitchstory story and story list objects you can generate
    documentation using a simple templating language. This example
    demonstrates how to generate markdown using jinja2.
  given:
    documentation.jinja2: |
      {% for story in story_list %}
      {{ story.name }}
      {{ "-" * story.name|length }}

      {{ story.about }}

      {% for name, property in story.given.properties.items()  %}
      {{ property.documentation }}
      {% endfor %}
      {% for step in story.steps %}
      {{ step.documentation }}
      {% endfor %}
      {% endfor %}
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
                Template(Path("documentation.jinja2").text()).render(
                    story_list=StoryCollection(
                        pathquery(".").ext("story"), Engine()
                    ).non_variations().ordered_by_file()
                )
            )
          will output: |-
            Login
            -----

            Simple log in.


            Load: /loginurl



            - Enter text 'AzureDiamond' in username.
            - Enter text 'hunter2' in password.

            * Click on login


            Log in on another url
            ---------------------

            Alternate log in URL.


            Load: /alternativeloginurl



            - Enter text 'AzureDiamond' in username.
            - Enter text 'hunter2' in password.

            * Click on login


            Log in as president
            -------------------

            For stories that involve Trump.


            Load: /loginurl



            - Enter text 'DonaldTrump' in username.
            - Enter text 'iamsosmrt' in password.

            * Click on login
