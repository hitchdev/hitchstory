with_documentation necessary:
  based on: Base documentation
  steps:
  - run:
      code: |
        print(
            jenv.from_string(Path("index.jinja2").text()).render(
                story_list=story_collection.ordered_by_file()
            )
        )
      raises:
        type: hitchstory.exceptions.WithDocumentationMissing
        message: Documentation templates missing. Did you use .with_documentation?

Template error:
  based on: Base documentation
  about: |
    If errors are raised in the template then display them
    clearly to the user.

  variations:
    in story:
      given:
        files:
          document.yaml: |
            story: |
              # {{ name }}
              
              {{ nonexistentvar }}
      steps:
      - run:
          code: |
            print(
                jenv.from_string(Path("index.jinja2").text()).render(
                    story_list=story_collection.with_documentation(
                        Path("document.yaml").text()
                    ).ordered_by_file()
                )
            )
          raises:
            type: hitchstory.exceptions.DocumentationTemplateError
            message: |-
              Exception in 'story' template.

              jinja2.exceptions.UndefinedError
              'nonexistentvar' is undefined
    in info:
      given:
        files:
          document.yaml: |
            story: |
              # {{ name }}
              
              {{ info.jiras.documentation() }}
            info:
              jiras: |
                {% for jira in jiras -%}
                * https://yourproject.jira.com/JIRAS/{{ non_existent_var }}
                {% endfor %}

      steps:
      - run:
          code: |
            print(
                jenv.from_string(Path("index.jinja2").text()).render(
                    story_list=story_collection.with_documentation(
                        Path("document.yaml").text()
                    ).ordered_by_file()
                )
            )
          raises:
            type: hitchstory.exceptions.DocumentationTemplateError
            message: |-
              Exception in 'info/jiras' template.

              jinja2.exceptions.UndefinedError
              'non_existent_var' is undefined
