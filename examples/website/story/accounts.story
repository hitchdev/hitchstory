Login:
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
  - load website: login/

  - enter:
      text: admin
      on: username
      
  - enter:
      text: password
      on: password

  - click: submit
  
  - page appears: main page
