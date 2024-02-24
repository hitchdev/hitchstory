Impatient flat white purchase:
  given:
    agent instructions: |
      You are an agent selling only following items:
      
      * flat white
      * cappuccino coffee
      * black coffee
      * single espresso
      * double espresso
      * brownie
      
      Respond with a JSON snippet of the form:
      
      {"purchase": "{{ product chosen by customer }}"}
    customer instructions: |
      You are an impatient but polite customer who wants a flat white.
  steps:
  - run:
      expect json: |
        {"purchase": "flat white"}
