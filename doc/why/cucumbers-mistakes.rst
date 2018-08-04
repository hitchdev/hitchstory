

What Cucumber/Gherkin got right
===============================

Emphasis on readability of the specs
------------------------------------



The idea that specifications should be executable and double as tests
---------------------------------------------------------------------


The deliberate use of a simplified configuration language for specifications
----------------------------------------------------------------------------

Deliberate separation of concerns between specification and story execution
---------------------------------------------------------------------------


Parameterization
----------------

The idea that the notion of specifications, tests and documentation are all intrinsically linked
------------------------------------------------------------------------------------------------


What Cucumber/Gherkin got wrong
===============================

Syntax Design
-------------

English is vague. English is verbose. English is messy. English is not strongly typed.

Like actual code, specifications need to be precise. Specifications need to be DRY. Specifications need to be exact. Whether executable or not.

Making English the basis of an executable specification language was only going to bring out the worst o

The first attempt at making a programming language that looked like English - COBOL - ended up being one of the hardest programming languages to learn.

Gherkin is not as bad as COBOL - it is a configuration language that tried to look like English - not a programming language.

Because of the ambiguous syntax design, there is no clear mapping between step definitions and 

The use of Given/When/Then/And as BDD training wheels that never come off
-------------------------------------------------------------------------

BDD emphasizes the notion of using Given, When and Then as a way of structuring example based test cases.

And, to be fair, almost every test case should follow this pattern.

However, making these keywords which are used to emphasize the structure every test case should follow
part of the language itself simply adds unnecessary syntactic noise.

For this reason, hitchstory doesn't use this syntax. You're encouraged to follow the structure of
*thinking* about "given, when, then", but to codify it as:

  given:
    something: something else
  steps:
  - step 1 # when
  - step 2 # then
  - step 3 # and
  - step 4 # but

The keyword 'given' is still used to distinguish parameters used to set up the environment from steps.

Why does this matter? It results in shorter test cases which means less code to manage.

This does not seem as important looking at one user story - multiply that by a thousand and you have
a lot more code.




No inheritance
--------------

  https://stackoverflow.com/questions/41872376/can-a-cucumber-feature-file-inherit-from-a-parent-feature-file
  
  "The short answer, no. Feature files can't inherit from another feature file."


Inheritance is about keeping code DRY. Specifications are configuration and just like
programming code, configuration is best kept DRY.

From the Stack overflow question:

  "A common background is to login in a system. Login is important but it can often be hidden in the steps."
  
It *can* be.

It *shouldn't* be.

The steps that lead to login are part of the specification of the system, so *why should it be hidden*?

This conflict between the desire to keep steps DRY and not hide meaningful details in steps
puts users of Cucumber in a horrible and unnecessary position.

In this article: https://makandracards.com/makandra/18905-how-to-not-repeat-yourself-in-cucumber-scenarios

I see somebody valiantly *struggling* to find a solution to "how can we achieve the same thing as
inheritance?" and finding 4 mediocre equivalents.


The idea that test cases should necessarily be non-technical
------------------------------------------------------------

Most software doesn't actually interact with humans it interacts with other software.

This interaction can be via code - in which case the specification ought to be defined
with snippets of code.

The interaction might instead be with a REST API - in which case, in order to be able
to define the interaction, you must understand and define the semantics of REST APIs
and be able to write them out if you are defining a spec.

The specification should not attempt to conceal or dumb down these details.

To be fair, this isn't a problem with the syntax of Gherkin or design of Cucumber
- it is mostly a cultural affectation.


Programmers need to want to use it even if the business isn't interested
------------------------------------------------------------------------

Due to all of the above problems, Gherkin does not have a wide adoption among developers.

It's not like deliberately simplified languages are not popular with developers for
other forms of configuration.

If programmers don't like using a tool or technology that interfaces to their code,
forget about getting the business to use it.

