---
title: Domain Appropriate Scenario Language (DASL)
---
# Domain Appropriate Scenario Language (DASL)


!!! note "#intro"

    "Strictly considered, writing about music is as illogical as singing about economics" - 1918 February 9, The New Republic, The Unseen World by H. K. M.


A domain appropriate scenario language is a formal, declarative DSL which can, for a particular application, define behavioral scenarios **clearly**, **unambiguously**, **concisely** and **precisely**.

A DASL is a key tool for the practice of carnivorous BDD.

While a DASL is not strictly *necessary* for writing code, without one it is easier for specification bugs to creep in. For example:

- Scenario descriptions that are unclear - ambiguous and missing key details ("missing meat").
- Scenario descriptions that are too verbose to be useful.
- Scenario descriptions that contain noise - extraneous information not relevant to the scenario description (e.g. implementation details).

With a DASL, it is also usually straightforward to execute the specifications from the example scenarios as tests.


## Gherkin is not good for DASLs

Gherkin is not useful for carnivorous BDD.

Gherkin, by dint of trying to express "English-like" requirements, is usually *not* a domain appropriate scenario language. This usually manifests in missing context about the spec. For example, a canonical example drawn from Cucumber training materials exhibit's this problem:

```gherkin
  Scenario: Create a new person
    Given API: I create a new person
    Then API: I check that POST call body is "OK"
    And API: I check that POST call status code is 200
```

This story omits several key details relevant to the scenario. *How* is a new person created? What *kind* of POST request is made? What response comes back with the 200 code?

Worse, it is misleading - not every attempt to create a new person will result in a 200. If the age is left out maybe it is not *supposed* to result in a 200. Or it it?

While Gherkin can in theory represent very precisely described scenarios, in practice stories will become overly verbose if you do. This is partly because Gherkin has no concept of inheritance.




## English is not a DASL

While spoken and written English can describe context and behavioral scenarios at a high level (as is done above with the "about" section), if an entire scenario is described this way then key information will often be lost.

The rigidity of a DASL as compared to English helps ensure that the specification gaps are filled in.




## HitchStory as a tool for creating DASLs

The following is an example scenario written with a hitchstory StrictYAML DASL for describing the behavior of a REST API service:

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
        content: |
          {
            "name": "Thomas Kettering",
            "age": 35,
            "address": "1 Example road, example drive"
          }
    
      response:
        status: 200
        content: |-
          {
            "code": 200,
            "id": "e30ffb2-bb50-4836-aefa-86c78af157cc",
            "status": "success"
          }

        varying:
          id: thomas kettering's user id

  - API call:
      request:
        username: john
        method: GET
        path: /employee/{{ thomas kettering's user id }}
      response:
        status: 200
        content: |-
          {
            "id": "e30ffb2-bb50-4836-aefa-86c78af157cc",
            "name": "Thomas Kettering",
            "age": 35,
            "address": "1 Example road, example drive"
           }
         varying:
           id: thomas kettering's user id
  
```



