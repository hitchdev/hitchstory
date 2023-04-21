Correct my spelling:
  about: |
    In this story we call the API and send it misspellings.

    The API uses TextBlob (https://textblob.readthedocs.io/en/dev/)
    to detect misspellings and replies to the API with a suggestion
    instead of adding it to the to do list.
  steps:
  - expect: Enter your choice

  - display: |-
      To-do list:
      Options:
      1. Add item
      2. Remove item
      3. Quit
      Enter your choice:

  - enter text: 1

  - expect: Enter a to-do item

  - enter text: biuy breod

  - expect: Did you mean "buy bread"?

  - display: |-
      To-do list:
      Options:
      1. Add item
      2. Remove item
      3. Quit
      Enter your choice: 1
      Enter a to-do item: biuy breod
      Did you mean "buy bread"?
      Enter Y to confirm, or any other key to re-enter:


  - expect: Enter Y to confirm

  - enter text: Y

  - display: |-
      To-do list:
      Options:
      1. Add item
      2. Remove item
      3. Quit
      Enter your choice: 1
      Enter a to-do item: biuy breod
      Did you mean "buy bread"?
      Enter Y to confirm, or any other key to re-enter: Y
      To-do list:
      1. buy bread
      Options:
      1. Add item
      2. Remove item
      3. Quit
      Enter your choice:


  - enter text: 3

  - exit successfully
