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
