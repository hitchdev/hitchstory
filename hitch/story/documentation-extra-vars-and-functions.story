Generate documentation with extra variables and functions:
  based on: base documentation
  docs: documentation/extra
  status: experimental
  about: |
    Using extra=, you can use additional functions and variables
    defined outside of the template.
  given:
    files:
      document.yaml: |
        story: |
          # {{ name }}
          
          URL : {{ WEBSITE }}/stories/{{ slug }}.html
          
          {{ info.jiras.documentation() }}

          {{ about }}
        info:
          jiras: |
            {% for jira in jiras -%}
            * {{ jira_url(jira) }}
            {% endfor %}
  steps:
  - run:
      code: |
        extra = {
            "WEBSITE": "http://www.yourdocumentation.com/",
            "jira_url": lambda jira: f"https://yourproject.jira.com/JIRAS/{jira}",
        }

        print(
            jenv.from_string(Path("index.jinja2").text()).render(
                story_list=story_collection.with_documentation(
                    Path("document.yaml").text(), extra=extra
                ).ordered_by_file()
            )
        )
      will output: |-
        # Login

        URL : http://www.yourdocumentation.com//stories/login.html

        * https://yourproject.jira.com/JIRAS/AZT-344
        * https://yourproject.jira.com/JIRAS/AZT-345


        Simple log in.

        # Log in on another url

        URL : http://www.yourdocumentation.com//stories/log-in-on-another-url.html

        * https://yourproject.jira.com/JIRAS/AZT-344
        * https://yourproject.jira.com/JIRAS/AZT-589


        Alternate log in URL.

        # Log in as president

        URL : http://www.yourdocumentation.com//stories/log-in-as-president.html

        * https://yourproject.jira.com/JIRAS/AZT-611


        For stories that involve Trump.
