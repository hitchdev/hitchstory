Espresso purchase:
  based on: basic barista
  steps:
  - speak:
      message: Can I order an espresso?
      expect json: |-
        {"purchase": "single espresso"}

Try to order a pizza:
  based on: basic barista
  steps:
  - speak:
      message: Can I order a pizza?
      expect answer:
        - question: Did the barista let you order a pizza? Answer yes or no.
          response: no
        - question: Was the barista polite? Answer yes or no.
          response: yes

Order a pizza, change my mind order a brownie:
  based on: basic barista
  steps:
  - speak:
      previous:
      - user: Can I order a pizza?
      - assistant: I'm sorry, but we only sell flat white, cappuccino coffee, black coffee, single espresso, double espresso, and brownie.
      message: Ok, how about a brownie?
      expect json: |-
        {"purchase": "brownie"}

Try to order a cookie:
  based on: basic barista
  steps:
  - speak:
      message: Can I order a cookie?
      expect answer:
        - question: Did the barista let you order a cookie? Answer yes or no.
          response: no
