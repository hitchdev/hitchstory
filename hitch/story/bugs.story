Re-use of with_documentation fails:
  about: |
    Original bug - second .ordered_by_file() would
    result in WithDocumentationMissing exception.
  based on: base documentation
  steps:
  - Run:
      code: |
        print(
            jenv.from_string(Path("index.jinja2").read_text()).render(
                story_list=story_collection.with_documentation(
                    Path("document.yaml").read_text(),
                ).ordered_by_file()
            )
        )

        print(
            jenv.from_string(Path("index.jinja2").read_text()).render(
                story_list=story_collection.with_documentation(
                    Path("document.yaml").read_text(),
                ).ordered_by_file()
            )
        )

Rewrite step in inherited story:
  based on: Story that rewrites itself
  given:
    files:
      inherited.story: |
        Following steps:
          based on: Append text to file
          following steps:
          - run and get output:
              command: cat mytext.txt
              will output: old value

  replacement steps:
  - Run:
      code: |
        StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True)).named("Following steps").play()
      will output: RUNNING Following steps in /path/to/working/inherited.story ...
        SUCCESS in 0.1 seconds.


  - File contents will be:
      filename: inherited.story
      contents: |-
        Following steps:
          based on: Append text to file
          following steps:
          - run and get output:
              command: cat mytext.txt
              will output: |-
                hello
                hello


