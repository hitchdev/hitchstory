Differences to Gherkin
======================

HitchStory and Gherkin are both DSLs for writing user stories that double as
acceptance tests, but they have different philosophies and approach.

Gherkin scenarios emphasize the following values:

* The use of English to facilitate customer collaboration.
* Showing information that is "interesting to the business".

Here are some examples.

From wikipedia:

.. code-block:: gherkin

    Scenario: Eric wants to withdraw money from his bank account at an ATM
        Given Eric has a valid Credit or Debit card
        And his account balance is $100
        When he inserts his card
        And withdraws $45
        Then the ATM should return $45
        And his account balance is $55

From the Cucumber website:
        
.. code-block:: gherkin
        
    Feature: Serve coffee
      Coffee should not be served until paid for
      Coffee should not be served until the button has been pressed
      If there is no coffee left then money should be refunded

    Scenario: Buy last coffee
      Given there are 1 coffees left in the machine
      And I have deposited 1$
      When I press the coffee button
      Then I should be served a coffee
    
Hitch scenarios, by contrast, emphasizes the following values:

* The screenplay principle of "show everything that the user can see or hear".
* The *generation* of documentation for customer collaboration and stakeholders input.
* Terseness of code and DRY.

Equivalent scenarios:

.. code-block:: yaml
    
    Withdraw money from ATM:
      with:
        card: barclays card 148
      given:
        card: (( card ))
        account balance: $100
      steps:
      - Insert card
      - Withdraw: $45
      - ATM returns: $45
      - Account balance: $55
  
  
.. code-block:: yaml


    Buy last coffee:
      given:
        machine contains:
          coffees: 1
      steps:
      - Deposit: $1
      - Press button: coffee
      - Served up: coffee
