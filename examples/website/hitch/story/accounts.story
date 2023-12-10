# If you remove .only_uninherited() at the end
# of test_integration.py this story will be turned
# into a test - "test_login" just like all the 
# other stories are.

# Because it is used in other tests, it's assumed
# that it doesn't need to be run by itself.

Login:
  about: |
    Login as admin user.
  given:
    browser: chromium
    data:
      todos.todo:
        10:
          title: Buy peppers
          created_at: 2023-01-01T00:00:00.000Z
          update_at: 2023-01-01T00:00:00.000Z
          isCompleted: no
        11:
          title: Buy cereal
          created_at: 2023-01-01T00:00:00.000Z
          update_at: 2023-01-01T00:00:00.000Z
          isCompleted: yes
  steps:
  - load website: login/

  - page appears: login

  - enter:
      text: admin
      on: username
      
  - enter:
      text: password
      on: password

  - click: submit
  
  - page appears: dashboard 
  
  - should appear:
      on: title
      text: Todo List

