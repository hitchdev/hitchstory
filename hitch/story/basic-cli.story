Creating a basic command line test runner:
  docs: setup/basic-cli
  based on: quickstart
  about: |
    This example demonstrates the stories in the README
    being run via a command line runner. It can be directly
    copied and pasted.

    This is useful if you want to run the tests outside of
    pytest.

    It uses the popular [click](https://click.palletsprojects.com/)
    package to interpret command line arguments.
  given:
    files:
      runner.py: |
        from hitchstory import StoryCollection
        from click import argument, group, pass_context
        from engine import Engine
        from pathlib import Path

        THIS_DIR = Path(__file__).absolute().parents[0]

        STORIES = THIS_DIR.glob("*.story")

        @group(invoke_without_command=True)
        @pass_context
        def cli(ctx):
            """Integration test command line interface."""
            pass

        @cli.command()
        @argument("keywords", nargs=-1)
        def atdd(keywords):
            """
            Run single story with name matching keywords.
            """
            StoryCollection(STORIES, Engine())\
                .shortcut(*keywords)\
                .play()

        @cli.command()
        @argument("keywords", nargs=-1)
        def ratdd(keywords):
            """
            Run single story with name matching keywords in rewrite mode.
            """
            StoryCollection(STORIES, Engine())\
                .shortcut(*keywords)\
                .play()

        @cli.command()
        def regression():
            """
            Run all tests.
            """
            StoryCollection(STORIES, Engine())\
                .only_uninherited()\
                .ordered_by_name()\
                .play()


        if __name__ == "__main__":
            cli()

  variations:
    Regular ATDD:
      about: Run a single test.
      replacement steps:
      - run python:
          args: runner.py atdd email sent
          will output: |-
            RUNNING Email sent in /path/to/example.story ... Load web page at /login
            Put hunter2 in name
            Put AzureDiamond in name
            Click on login
            Click on new email
            Put Hey guys,

            I think I got hacked!
             in name
            Put Cthon98@aol.com in name
            Click on send email
            Check email was sent!
            SUCCESS in 0.1 seconds.

    Rewrite ATDD:
      about: Run a single test in rewrite mode.
      replacement steps:
      - run python:
          args: runner.py ratdd email sent
          will output: |-
            RUNNING Email sent in /path/to/example.story ... Load web page at /login
            Put hunter2 in name
            Put AzureDiamond in name
            Click on login
            Click on new email
            Put Hey guys,

            I think I got hacked!
             in name
            Put Cthon98@aol.com in name
            Click on send email
            Check email was sent!
            SUCCESS in 0.1 seconds.

    Regression:
      about: Run all tests.
      replacement steps:
      - run python:
          args: runner.py regression
          will output: |-
            RUNNING Email sent in /path/to/example.story ... Load web page at /login
            Put hunter2 in name
            Put AzureDiamond in name
            Click on login
            Click on new email
            Put Hey guys,

            I think I got hacked!
             in name
            Put Cthon98@aol.com in name
            Click on send email
            Check email was sent!
            SUCCESS in 0.1 seconds.
