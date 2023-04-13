---
title: Test concern leakage
---
# Test concern leakage

Test concern leakage is when there is an enforced [separatism of test concerns](../separation-of-test-concerns) but specification code is pushed into execution code or vice versa.

In general, xUnit code maintain no separation of concerns.


## Downward concern leakage

Downward concern leakage is the most common form of concern leakage - where elements of behavior are pushed down from the specification language to the code that executes the test.

For example (drawn from a Cucumber tutorial), this story exhibits downward concern leakage:

```gherkin
  Scenario: Create a new person
    Given API: I create a new person
    Then API: I check that POST call body is "OK"
    And API: I check that POST call status code is 200
```

*How* a new person is created here is left entirely open ended. Indeed, it's likely that there are many different ways that one could try to create a new person using an API that would not result in a status code of 200.

Cucumber stories in fact, *usually* exhibit this problem, as the the inexpressivity of the language prevents complex specifications from being represented.

The step code used to exercise this story *is* precise about these things and the end user will certainly know what they are but it is left to the reader's imagination what they actually are.

An equivalent hitchstory that has no downward concern leakage would include more details:

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



