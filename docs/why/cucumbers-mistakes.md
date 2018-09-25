---
title: Why not use Behave, Lettuce or Cucumber (Gherkin)?
---

HitchStory and Gherkin are both DSLs for writing user stories that can double as
acceptance tests, but they have different philosophies and approach.

Gherkin scenarios emphasize the following values:

* The use of English to facilitate customer collaboration.
* Showing information that is "interesting to the business".

Here are some examples.

From the Cucumber website:

```gherkin
Scenario: Buy last coffee
  Given there are 1 coffees left in the machine
  And I have deposited 1$
  When I press the coffee button
  Then I should be served a coffee
```

Hitch scenarios, by contrast, emphasizes the following values:

* Ease of use and maintenance by developers first.
* The screenplay principle.
* Terse, DRY code.
* The generation of documentation for customer collaboration and stakeholders input from specifications.

Equivalent scenarios:

```yaml
Buy last coffee:
  given:
    machine contains:
      coffees: 1
  steps:
  - Deposit: $1
  - Press button: coffee
  - Served up: coffee
```

# What Cucumber/Gherkin got wrong

## Being an English-like language

English is vague. English is verbose. English is messy. English is imprecise. These are ideal qualities for some purposes but they are not ideal for writing specifications.

Like actual code, to be effective, specifications must be exact, precise and DRY - whether executable or not.

The imprecision of English is drawn out in Gherkin specifications - they usually lack precision and critical details and end up serving as a sort of high level description of what the program it's describing does.


## Parser hell

   Some people, when confronted with a problem, think "I know, I'll use regular expressions." Now they have two problems. - Jamie Zawinksi

Because of the Englishy nature of the language, parsing is also difficult. Gherkin requires very 

There are a multiplicity of examples around the web where it went wrong causing many headaches for users of Cucumber
and often leading to hours of unnecessary debugging and [workarounds](http://coryschires.com/ten-tips-for-writing-better-cucumber-steps/).

One of the facets of the syntactic ambiguity is that some parsers require you to write regular expressions to parse segments
of the Gherkin.


## Given/When/Then/And are BDD training wheels that don't come off

BDD emphasizes the notion of using Given, When and Then as a way of structuring example based test cases.

And, to be fair, almost every test case *should* follow this pattern. However, these keywords do not hold
any meaning for the parser and are ignored.

For this reason, hitchstory advocates the Given/When/Then *pattern* but, apart from 'given' does not use these
keywords. "Given" is a user defined mapping of arbitrary YAML that can be used to configure how set_up behaves,
while the meat of the stories is in the steps.

  given:
    something: something else
  steps:
  - step 1 # when
  - step 2 # then
  - step 3 # and
  - step 4 # but

Why does this matter? It results in executable specifications which are naturally terser and which have more
room for your business logic.


## Verbosity

## Weakly typed

## No inheritance

  https://stackoverflow.com/questions/41872376/can-a-cucumber-feature-file-inherit-from-a-parent-feature-file
  
  "The short answer, no. Feature files can't inherit from another feature file."

Inheritance is, and always has been about keeping code DRY. It is a thorny tool because, while it can reduce
repetition it can sacrifice readability. For this reason, Gherkin left it out.

From the Stack overflow question:

  "A common background is to login in a system. Login is important but it can often be hidden in the steps."

It *can* be.

It *shouldn't* be.

The steps that lead to login are part of the specification of the system, so *why should it be hidden*?

This conflict between the desire to keep steps DRY and not hide meaningful details in steps
puts users of Cucumber in a horrible and unnecessary position.

In the article [how not to repeat yourself in cucumber scenarios](https://makandracards.com/makandra/18905-how-to-not-repeat-yourself-in-cucumber-scenarios)
I see somebody valiantly *struggling* to find a solution to "how can we achieve the same thing as
inheritance?" and finding 4 mediocre equivalents.

## The idea that executable specifications should necessarily be non technical

  Talking about music is like dancing about architecture -- Marvin Mull

Most software packages under test don't actually interact with humans they interacts with other software.

This interaction can be via code - in which case the specification ought to be defined
with snippets of code.

The interaction might instead be with a REST API - in which case, in order to be able
to define the interaction, you must understand and define the semantics of REST APIs
and be able to write them out if you are defining a spec.

The specification should not attempt to conceal or dumb down these details.

To be fair, this isn't a problem with the syntax of Gherkin or design of Cucumber
- it is mostly a cultural affectation.


## Programmers need to want to use the executable specification tool even if the business isn't interested

Due to all of the above problems, Gherkin does not have a wide adoption among developers.

It's not like deliberately simplified languages are not popular with developers for
other forms of configuration.

If programmers don't like using a tool or technology that interfaces to their code,
forget about getting the business to use it.



## What Gherkin got right

Cucumber and their related tools became popular for good reasons, even though they made
many mistakes. They also got a lot of (non-obvious) stuff right:

* Emphasis on readability of the specs

* The idea that specifications should be executable and double as tests

* The deliberate use of a simplified configuration language for specifications

* Deliberate separation of concerns between specification and story execution

* Built in Parameterization

* The idea that the notion of specifications, tests and documentation are all intrinsically linked
