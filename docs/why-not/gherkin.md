---
title: Why not use Behave, Lettuce or Cucumber (Gherkin)?
---

HitchStory and Gherkin are both DSLs for writing user stories that can double as
acceptance tests, but they have slightly different philosophies and approach.

Gherkin's philosophy emphasize the following values:

* The use of English to facilitate customer collaboration.
* Showing information that is "interesting to the business".

Whereas hitchstory's philosophy emphasizes very *similar* values, with some important differences:

* The use of [typed YAML](../../why/strictyaml) to define specs for readability, precision, clarity, terseness and ease of maintenance.

* Specifying all behavior precisely as per the [screenplay principle](../../approach/screenplay-principle).

* Templated documentation generation from specs and/or code artefacts to communicate information that is interesting to stakeholders.


## What Gherkin got right

Cucumber and their related tools became popular for good reasons, even though they made
many mistakes. They also got a lot of non-obvious stuff right:

* Emphasis on readability of the specs - something that unit tests typically fail at.

* The idea that specifications should double as tests.

* The deliberate use of a simpler non-turing complete language for specifications.

* The separation of concerns between specification and story execution.

* Built in parameterization.

* The idea that the notion of specifications, tests and documentation are all intrinsically linked.


## Example gherkin code vs hitchstory

From [the training wheels come off](http://aslakhellesoy.com/post/11055981222/the-training-wheels-came-off),
Aslak Hellesøy described how Cucumber was used to write tests (in his view, poorly):

```gherkin
Scenario: Successful login
  Given a user "Aslak" with password "xyz"
  And I am on the login page
  And I fill in "User name" with "Aslak"
  And I fill in "Password" with "xyz"
  When I press "Log in"
  Then I should see "Welcome, Aslak"
```

And how he thinks it should be used:

```gherkin
Scenario: User is greeted upon login
  Given the user "Aslak" has an account
  When he logs in
  Then he should see "Welcome, Aslak"
```

Equivalent scenario in hitchstory:

```yaml
Aslak sees welcome message on login:
  steps:
  - visit: /login
  - fill form:
      username: Aslak
      password: xyz
  - click: log in button
  - should contain:
      item: welcome banner
      message: Welcome, Aslak
```

# What Cucumber/Gherkin got wrong

## Being an English-like language

English is vague. English is verbose. English is messy. English is imprecise. These are ideal qualities for some purposes but they are not ideal for writing specifications.

Like actual code, to be effective, specifications are exact, precise and DRY. Even non-executable specifications
benefit from these qualities.

The imprecision of English is drawn out in Gherkin specifications partly due to its lack of inheritance. This
encourages vague 

- they usually lack precision and critical details and end up serving as a sort of high level description of what the program it's describing does.


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


