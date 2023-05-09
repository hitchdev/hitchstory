Existing todos:
  about: |
    This story doesn't have any steps and won't run,
    but it provides some todos which child stories
    that are "based upon" it can use.
  given:
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


Add and retrieve todo:
  about: |
    The user adds "buy bread" to the to do list
    and sees it showing up.
    
  # custom metadata
  jiras: FEATURE-341, FEATURE-441
  docs: yes # for interesting stories
  
  based on: existing todos  # all of the other data
  given:
    browser: webkit
    data:
      todos.todo:
        # Also includes peppers and cereal
        12:
          title: Buy a toaster
          created_at: 2023-05-08T16:29:41.595Z
          update_at: 2023-05-08T16:29:41.595Z
          isCompleted: yes

  steps:
  - load website: todos/

  - enter:
      on: todo text
      text: Add bread

  - click: add

  - should appear:
      text: Add bread
      on: todo list item
      which: 0
