Add and retrieve todo:
  about: |
    The user adds "buy bread" to the to do list
    and sees it showing up.
  jiras: FEATURE-341, FEATURE-441    # custom metadata
  given:
    browser: chromium
    data:
      todos.todo:
        10:
          title: Buy peppers
          created_at: 2023-05-08T16:29:41.595Z
          update_at: 2023-05-08T16:29:41.595Z
          isCompleted: no
        11:
          title: Buy cereal
          created_at: 2023-05-08T16:29:41.595Z
          update_at: 2023-05-08T16:29:41.595Z
          isCompleted: yes
          
  steps:
  - load website: todos

  - enter:
      on: todo text
      text: Add bread

  - click: add

  - should appear:
      text: Add bread
      on: todo list item
      which: 0
