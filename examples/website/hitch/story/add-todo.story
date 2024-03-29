Add and retrieve todo:
  about: |
    The user adds "buy bread" to the to do list
    and sees it showing up.
    
  # custom metadata
  jiras: FEATURE-341, FEATURE-441
  docs: yes # turn this story into markdown docs
  
  # inherit from login story in accounts.story
  based on: login

  given:
    browser: chromium
    data:
      todos.todo:
        # Also includes peppers and cereal from "Login"
        12:
          title: Buy a toaster
          created_at: 2023-01-01T00:00:00.000Z
          update_at: 2023-01-01T00:00:00.000Z
          isCompleted: yes

  following steps:
  - enter:
      on: todo text
      text: Add bread

  - click: add

  - should appear:
      text: Add bread
      on: first todo list item
