Base documentation:
  given:
    files:
      example.story: |
        Login:
          about: Simple log in.
          jiras: AZT-344, AZT-345
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
          - Click:
              item: right
              double: yes


        Log in on another url:
          about: Alternate log in URL.
          jiras: AZT-344, AZT-589
          based on: login
          given:
            url: /alternativeloginurl

        Log in as president:
          about: For stories that involve Trump.
          jiras: AZT-611
          based on: login
          with:
            username: DonaldTrump
            password: iamsosmrt
      engine.py: |
        from hitchstory import BaseEngine, GivenDefinition, GivenProperty
        from hitchstory import InfoDefinition, InfoProperty, validate
        from strictyaml import Map, Int, Str, Bool, Optional, CommaSeparated


        class Engine(BaseEngine):
            given_definition = GivenDefinition(
                url=GivenProperty(schema=Str()),
            )
            
            info_definition = InfoDefinition(
                jiras=InfoProperty(schema=CommaSeparated(Str())),
            )

            def set_up(self):
                print("visit {0}".format(self.given['url']))

            def fill_form(self, **textboxes):
                for name, text in sorted(textboxes.items()):
                    print("with {0}".format(name))
                    print("enter {0}".format(text))
              
            def drag(self, from_item, to_item):
                print(f"drag {from_item} to {to_item}")

            @validate(double=Bool())
            def click(self, item, double=False):
                if double:
                    print(f"double clicked on {item}")
                else:
                    print(f"clicked on {item}")

      index.jinja2: |
        {% for story in story_list %}
        {{ story.documentation() }}
        {% endfor %}
      document.yaml: |
        story: |
          # {{ name }}
          
          {{ info.jiras.documentation() }}

          {{ about }}

          {% for name, property in given.items() %}
          {{ given[name].documentation() }}
          {% endfor %}
          {% for step in steps %}
          {{ step.documentation() }}
          {% endfor %}
          
          ## Automatically generated
          
          Automatically generated from {{ filename.name }}
        info:
          jiras: |
            {% for jira in jiras -%}
            * https://yourproject.jira.com/JIRAS/{{ jira }}
            {% endfor %}
        given:
          url: 'Load: {{ url }}'
        steps:
          fill form: |-
            {% for name, value in textboxes.items() %}
            - Enter text '{{ value }}' in {{ name }}.
            {%- endfor %}
            
            ![](screenshots/{{ this_story.slug }}-{{ this_step.index }}-{{ this_step.slug }}.png)
          click: |
            '* {% if double %}Double click{% else %}Click{% endif %} on {{ item }}'
            
            ![](screenshots/{{ this_story.slug }}-{{ this_step.index }}-{{ this_step.slug }}.png)
          drag: |
            '* Drag from {{ from_item }} to {{ to_item }}.'
            
            ![](screenshots/{{ this_story.slug }}-{{ this_step.index }}-{{ this_step.slug }}.png)
    setup: |
      from hitchstory import StoryCollection
      from pathlib import Path
      from engine import Engine
      from path import Path
      import jinja2

      jenv = jinja2.Environment(
          undefined=jinja2.StrictUndefined, loader=jinja2.BaseLoader
      )

      story_collection = StoryCollection(
          Path(".").glob("*.story"), Engine()
      ).non_variations()

Generate documentation from story:
  based on: base documentation
  docs: documentation/generate
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
  steps:
  - run:
      code: |
        print(
            jenv.from_string(Path("index.jinja2").text()).render(
                story_list=story_collection.with_documentation(
                    Path("document.yaml").text(),
                ).ordered_by_file()
            )
        )
      will output: |-
        # Login

        * https://yourproject.jira.com/JIRAS/AZT-344
        * https://yourproject.jira.com/JIRAS/AZT-345


        Simple log in.


        Load: /loginurl



        - Enter text '(( username ))' in username.
        - Enter text '(( password ))' in password.

        ![](screenshots/login-0-fill_form.png)

        '* Click on login'

        ![](screenshots/login-1-click.png)

        '* Drag from left to right.'

        ![](screenshots/login-2-drag.png)

        '* Double click on right'

        ![](screenshots/login-3-click.png)


        ## Automatically generated

        Automatically generated from example.story

        # Log in on another url

        * https://yourproject.jira.com/JIRAS/AZT-344
        * https://yourproject.jira.com/JIRAS/AZT-589


        Alternate log in URL.


        Load: /alternativeloginurl



        - Enter text '(( username ))' in username.
        - Enter text '(( password ))' in password.

        ![](screenshots/log-in-on-another-url-0-fill_form.png)

        '* Click on login'

        ![](screenshots/log-in-on-another-url-1-click.png)

        '* Drag from left to right.'

        ![](screenshots/log-in-on-another-url-2-drag.png)

        '* Double click on right'

        ![](screenshots/log-in-on-another-url-3-click.png)


        ## Automatically generated

        Automatically generated from example.story

        # Log in as president

        * https://yourproject.jira.com/JIRAS/AZT-611


        For stories that involve Trump.


        Load: /loginurl



        - Enter text '(( username ))' in username.
        - Enter text '(( password ))' in password.

        ![](screenshots/log-in-as-president-0-fill_form.png)

        '* Click on login'

        ![](screenshots/log-in-as-president-1-click.png)

        '* Drag from left to right.'

        ![](screenshots/log-in-as-president-2-drag.png)

        '* Double click on right'

        ![](screenshots/log-in-as-president-3-click.png)


        ## Automatically generated

        Automatically generated from example.story
