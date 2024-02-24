Buy coffee:
  based on: gpt4
  about: |
    Agent buys a coffee from customer.
  given:
    agent instructions: |
      You are an agent selling the following items:
      
      * Flat white coffee
      * 
    customer instructions: |
      You are an impatient customer who wants a flat white.
  steps:
  - run:
      expect json: |
        {"purchase": "flat white"}
