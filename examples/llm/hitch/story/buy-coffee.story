Impatient flat white purchase:
  given:
    agent instructions: |
      You are an agent selling the following items:
      
      * Flat white coffee
      * Cappuccino coffee
    customer instructions: |
      You are an impatient customer who wants a flat white.
  steps:
  - run:
      expect json: |
        {"purchase": "flat white"}
