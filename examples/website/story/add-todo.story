Add and retrieve todo:
  about: |
    The user adds "buy bread" to the to do list
    and sees it showing up.
  steps:
  - load website

  - enter:
      on: todo text
      text: Add bread

  - click: add

  - should appear:
      text: Add bread
      on: todo list item
      which: first
