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
            "data": {
              "id": "243e6384-298b-4443-a9c9-0cb5d18b92be",
              "timestamp": 1683888169
            },
            "message": "Item added successfully"
          }
        varying:
          data/id: uuid
          data/timestamp: timestamp

  - call api:
      request:
        method: GET
        path: /todo
      response:
        content: |
          [
            "buy bread"
          ]
