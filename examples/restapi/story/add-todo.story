Add and retrieve todo:
  about: |
    In this story we call the API to buy bread
    and then see that bread is on the list.
  steps:
  - call api:
      request:
        method: POST
        headers:
          Content-Type: application/json
        path: /todo
        content: |
          {
              "item": "buy bread"
          }

      response:
        content: |
          {
              "message": "Item added successfully"
          }

  - call api:
      request:
        method: GET
        path: /todo
      response:
        content: |
          [
            "buy bread"
          ]
