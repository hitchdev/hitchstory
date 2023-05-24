Correct my spelling:
  about: |
    The user tries to add "biuy breod" to the to do list
    but the application tries to correct the spelling.

  # custom metadata:
  docs: yes # for interesting stories
  context: |
    The website uses TextBlob (https://textblob.readthedocs.io/en/dev/)
    to detect misspellings and replies to the API with a suggestion
    instead of adding it to the to do list.

  based on: login

  following steps:
  - enter:
      on: todo text
      text: biuy breod

  - click: add

  - should appear:
      text: Did you mean 'buy bread'?
      on: error
