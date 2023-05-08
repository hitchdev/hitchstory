Add and retrieve todo:
  about: |
    The user adds "buy bread" to the to do list
    and sees it showing up.
  jiras: FEATURE-341, FEATURE-441    # custom metadata
  given:
    browser: chromium
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

  - pause
