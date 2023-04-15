---
title: Test concern leakage
---
# Test concern leakage

Test concern leakage is when there is an enforced [separatism of test concerns](../separation-of-test-concerns) where specification details are pushed into executable code or (the other way) implementation details are pushed into the story.

In general, xUnit tests do not enforce a separation of concerns.

Test concern leakage is commonly exhibited in storytests written with tools like Hitchstory, Robot or Cucumber, however.


## Downward concern leakage

Downward concern leakage is the most common form of concern leakage - where behavioral specification details are pushed down from the specification language to the code that executes the test.

For example, this story (plucked from a Cucumber tutorial) exhibits downward concern leakage:

```gherkin
  Scenario: Create a new person
    Given API: I create a new person
    Then API: I check that POST call body is "OK"
    And API: I check that POST call status code is 200
```

*How* a new person is created here is left entirely unspecified.

Cucumber stories *usually* exhibit this problem, unfortunately, as the the inexpressivity of the language prevents complex specifications from being represented.

The step code used to exercise this story *is* precise about these things but it will be pushed into the step code used to exercise these steps.

An equivalent hitchstory without downward concern leakage would include more details:

```yaml
Create a new person:
  steps:
  - Call api:
       request:
         method: POST
         path: /person/new
       request content: |-
         {
            "name": "Tom Jones",
            "dob": "1990-12-25",
            "type": "employee"
         }
       response:
         code: 200
       response content: |-
         {
           "status": 200
         }
```

This story is still missing some details that may be critical to the specification (e.g. authentication, request headers) but it is straightforward enough to add these - StrictYAML being flexible enough to allow for complex representations of data.




## Upward concern leakage

Upward concern leakage is where implementation details that are not about the user's behavior are "leaked" into the story.

This example is drawn from a real story on github, but is translated into hitchstory:

```yaml
Use select and deselect all buttons:
  based on: Logged in as teacher1
  steps:
  - Follow: Course 1
  - Follow: Participants
  - Click: Select all
  - Field with:
      xpath: //tbody//tr[1]//input[@class='usercheckbox']
      should be: 1
  - Field with:
       xpath: //tbody//tr[2]//input[@class='usercheckbox']
       should be: 1
```

Xpath selectors "pollute" the story here.

To mitigate this, some sort of label-xpath translation layer could be used, or the use of easier to read selectors.




## Why worry about test concern leakage at all?

Test concern leakage is probably not an existential problem for any project. If a project is well tested but has difficult to understand tests it is still well tested.

Nonetheless there are benefits to maintaining a strict separation of test concerns. With minimized downward leakage:

- Engine code that executes stories becomes a lot more generic and reusable.

- The specification is that much more accessible. This allows the stories to become part of a BDD-ATDD nexus - i.e. they become suitable for high level discussions about how the software should behave with a wider range of stakeholders.

- It lets you build out [triality](../triality) capabilities.



