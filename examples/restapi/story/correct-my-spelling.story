Correct my spelling:
  about: |
    In this story we call the API and send it misspellings.

    The API uses TextBlob (https://textblob.readthedocs.io/en/dev/)
    to detect misspellings and replies to the API with a suggestion
    instead of adding it to the to do list.
  steps:
  - call api:
      request:
        method: POST
        path: /todo
        headers:
          Content-Type: application/json

      request content: |
        {
            "item": "biuy breod"
        }

      response:
        code: 400

      response content: |
        {
          "message": "buy bread"
        }
      

  - call api:
      request:
        method: GET
        path: /todo
      response content: |
        []
