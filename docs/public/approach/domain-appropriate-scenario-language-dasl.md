---
title: Domain Appropriate Scenario Language (DASL)
---
# Domain Appropriate Scenario Language (DASL)


!!! note "#intro"

    "Strictly considered, writing about music is as illogical as singing about economics" - 1918 February 9, The New Republic, The Unseen World by H. K. M.


A domain appropriate scenario language is a formal declarative DSL which can be used to define behavioral scenarios **clearly**, **unambiguously**, **concisely** and **precisely**.

With a DASL, BDD 

Example:

```yaml
Add employee record:
  # business readable high level description
  about: |
    When an employee's key details are added via the employee api
    then that employee details can be retrieved via that API.

  # sequence of steps that leads to desired outcome
  steps:
  - API Call:
      request:
        username: john
        method: POST
        path: /employee/add
        # other relevant details of the API request may be added here

      request data:
        {
            "name": "Thomas Kettering",
            "age": 35,
            "address": "1 Example road, example drive"
        }
    
      response:
        status: 200
        # more data about the type of response can be added here if relevant

      response data: |-
        {
            "code": 200,
            "id": "e30ffb2-bb50-4836-aefa-86c78af157cc",
            "status": "success"
        }
      
      # In this above case, id is an example of an ID, not the
      # one that will actually be returned
      varying data:
        - id: thomas kettering's user id

  - API call:
      request:
        username: john
        method: GET
        path: /employee/{{ thomas kettering's user id }}
      response:
        status: 200
      
      # desired outcome
      response data: |-
        {
            "id": "e30ffb2-bb50-4836-aefa-86c78af157cc",
            "name": "Thomas Kettering",
            "age": 35,
            "address": "1 Example road, example drive"
        }
```

While spoken and written English can describe behavioral scenarios at a high level (as is done with the "about" section), if an entire test is described this way it will be prone to the kind of ambiguity that a DASL is not susceptible to.

Gherkin, by dint of trying to express Englishy requirements, is not a domain appropriate scenario language. This usually manifests in missing context.

Example equivalent Cucumber scenario (drawn from Cucumber training materials):

```gherkin
  Scenario: Create a new person
    Given API: I create a new person
    Then API: I check that POST call body is "OK"
    And API: I check that POST call status code is 200
```

This story omits several key details relevant to the scenario. For instance, *how* is a new person created? What kind of POST request is made? What response comes back with the 200 code?

If this were adjusted to be a bug report ("API returns 500 error when creating new person"), the missing context would be starkly obvious.

The above scenario exhibits downward concern leakage - key details of the specification are buried in the step code.

A DASL scenario will contain all relevant specification information for *any* stakeholder. E.g. in the above example it could include the consumers of the API consuming the mobile app.

