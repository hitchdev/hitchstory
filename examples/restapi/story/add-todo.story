Add and retrieve todo:
  about: |
    In this story we call the API to buy bread
    and then see that bread is on the list.
  steps:
  - call api:
      request:
        method: POST
        path: /todo
        headers:
          Content-Type: application/json

      request content: |
        {
            "item": "buy bread"
        }
      response content: |
        {
          "message": "Item added successfully"
        }

  - call api:
      request:
        method: GET
        path: /todo
      response content: |
        [
          "buy bread"
        ]
