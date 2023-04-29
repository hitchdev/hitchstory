Re-use of with_documentation fails:
  about: |
    Original bug - second .ordered_by_file() would
    result in WithDocumentationMissing exception.
  based on: base documentation
  steps:
  - Run:
      code: |
        print(
            jenv.from_string(Path("index.jinja2").text()).render(
                story_list=story_collection.with_documentation(
                    Path("document.yaml").text(),
                ).ordered_by_file()
            )
        )

        print(
            jenv.from_string(Path("index.jinja2").text()).render(
                story_list=story_collection.with_documentation(
                    Path("document.yaml").text(),
                ).ordered_by_file()
            )
        )

