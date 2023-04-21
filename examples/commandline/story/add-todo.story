Add and retrieve todo:
  about: |
    In this story we call the API to buy bread
    and then see that bread is on the list.
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

  - enter text: Buy bread

  - expect: Buy bread

  - display: |-
      To-do list:
      Options:
      1. Add item
      2. Remove item
      3. Quit
      Enter your choice: 1
      Enter a to-do item: Buy bread
      To-do list:
      1. Buy bread
      Options:
      1. Add item
      2. Remove item
      3. Quit
      Enter your choice:

  - enter text: 3

  - exit successfully
