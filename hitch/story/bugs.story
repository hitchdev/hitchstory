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


Rewrite story with replacement steps bug:
  based on: Story that rewrites itself
  given:
    files:
      example.story: |
        Append text to file:
          steps:
          - Run: echo hello >> mytext.txt
          - Run: echo hello >> mytext.txt
          - Run: echo hello >> mytext.txt

          variations:
            Output text to:
              replacement steps:
              - Run and get output:
                  command: cat mytext.txt
                  will output: 
  steps:
  - Run:
      code: |
        StoryCollection(Path(".").glob("*.story"), Engine(rewrite=True))\
          .named("Append text to file/Output text to").play()
      will output: |-
        RUNNING Append text to file/Output text to in /path/to/working/example.story ... SUCCESS in 0.1 seconds.

  - File contents will be:
      filename: example.story
      contents: |-
        Append text to file:
          steps:
          - Run: echo hello >> mytext.txt
          - Run: echo hello >> mytext.txt
          - Run: echo hello >> mytext.txt

          variations:
            Output text to:
              replacement steps:
              - Run and get output:
                  command: cat mytext.txt
                  will output: |-
                    hello
                    hello
