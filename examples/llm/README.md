# HitchStory LLM Tests Example

This example project demonstrates a skeleton for test driven prompt tuning
with [hitchstory](https://hitchdev.com/hitchstory).

There's a root story which has the prompt:

```
Basic barista:
  given:
    agent instructions: |
      You are a barista selling only following items:
      
      * flat white
      * cappuccino coffee
      * black coffee
      * single espresso
      * double espresso
      * brownie
      
      If a customer asks questions, tries to order something not
      on the list produce JSON of the form:
      
      {"message": "{{ your answer }}"}
      
      If a customer orders one of these, produce JSON
      of the form:
      
      {"purchase": "{{ product chosen by customer }}"}
```

Then there are child stories which inherit from it to test various scenarios:

```
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
```

The top story is entirely deterministic - there can only be one JSON output given the question. Anything else fails.

The bottom two can have a range of different acceptable responses, so I'm asking a *separate* LLM questions about the response. Its answers should be deterministic. For example, the same story run twice results in two different outputs:

```
$:~/hitch/story/examples/llm$ ./run.sh bdd cookie
RUNNING Try to order a cookie in /src/hitch/story/buy-coffee.story ... 
CUSTOMER : Can I order a cookie?
SERVER : {"message": "We only sell brownies"}
SUCCESS in 3.4 seconds.

$:~/hitch/story/examples/llm$ ./run.sh bdd cookie
RUNNING Try to order a cookie in /src/hitch/story/buy-coffee.story ... 
CUSTOMER : Can I order a cookie?
SERVER : {"message": "We only sell flat white, cappuccino coffee, black coffee, single espresso, double espresso, and brownie"}
SUCCESS in 3.6 seconds.
```

You can run the whole lot together (interactions are concealed in this case):

```
$:~/hitch/story/examples/llm$ ./run.sh regression
RUNNING Espresso purchase in /src/hitch/story/buy-coffee.story ... SUCCESS in 4.2 seconds.
RUNNING Try to order a cookie in /src/hitch/story/buy-coffee.story ... SUCCESS in 2.8 seconds.
RUNNING Try to order a pizza in /src/hitch/story/buy-coffee.story ... SUCCESS in 2.3 seconds.
```

## Quickstart

First install podman - it's required to run everything together.

`git clone git@github.com:hitchdev/hitchstory.git`

`cd hitchstory/examples/llm`

Grab an OpenAI API key from https://platform.openai.com/api-keys and put it in a new file called "hitchstory/examples/llm/hitch/OPENAI_API_KEY".

Run `./run.sh make` to set everything up.

## Self rewriting stories

Try changing the first story to "can I order an espresso?" to "can I order a flat white?" and run `./run.sh rbdd flat white`. This should adjust the expected JSON in the story.

You can hack on the .story files in story/ folder to create new scenarios and
engine.py to change the way the scenarios are executed, add new checks and more!


## Contents of this subproject

`hitch/story` -- contains YAML stories.

`hitch/engine.py` -- the execution engine for these stories. It's the director that interprets the stories. The stories are structured and typed according to the code here.

`hitch/llm.py` -- tools for the execution of OpenAI.

`hitch/cli.py` -- command line tools e.g. running single stories (bdd), single stories in rewrite mode (rbdd) and all stories together (regression).
