Flat white purchase:
  based on: basic barista
  steps:
  - speak:
      message: Can I order a flat white?
      expect json: |
        {"purchase": "flat white"}

Try to order a pizza:
  based on: basic barista
  steps:
  - speak:
      message: Can I order a pizza?
      expect answer:
        question: Did the barista let you order a pizza? Answer yes or no.
        response: no

Try to order a cookie:
  based on: basic barista
  steps:
  - speak:
      message: Can I order a cookie?
      expect answer:
        question: Did the barista let you order a cookie? Answer yes or no.
        response: no
