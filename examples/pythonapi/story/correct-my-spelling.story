Correct my spelling:
  about: |
    In this story we call the Python API and send it misspellings.

    The API uses TextBlob (https://textblob.readthedocs.io/en/dev/)
    to detect misspellings and raises an exception with a correction.
  steps:
  - run:
      code: |
        import todo
        todo.add_item("biuy breod")
      raises:
        type: todo.Misspelling
        message: Did you mean "buy bread"?
