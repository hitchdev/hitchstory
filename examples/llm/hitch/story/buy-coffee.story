Impatient flat white purchase:
  based on: basic barista
  given:
    customer instructions: |
      You are an impatient but polite customer who wants a flat white.
  steps:
  - expect json: |
      {"purchase": "flat white"}

Try to order a pizza:
  based on: basic barista
  given:
    customer instructions: |
      You are a customer. Try to order a pizza from a barista.
  steps:
  - expect message:
      question: Did the barista let you order a pizza? Answer yes or no.
      response: no
