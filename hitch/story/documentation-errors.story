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

Missing step:
  about: |
    * Check to see if there are steps/given/info there shouldnt be.
    * If it is not used in the template, it doesn't need to be there.
