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
        message: 3 'nonexistentvar' is undefined
