# HitchStory LLM Tests Example

This example project demonstrates a skeleton for test driven prompt tuning
with hitchstory.

## Quickstart

Install podman.

`git clone git@github.com:hitchdev/hitchstory.git`

`cd hitchstory/examples/llm`

Put your OPENAI_API_KEY In the file "hitchstory/examples/llm/hitch/OPENAI_API_KEY".

Run `./run.sh make` to set everything up.

## Try it out

Run `./run.sh bdd espresso`

Run `./run.sh bdd pizza`

Run `./run.sh bdd cookie`

Run `./run.sh regression`

It should run all of the stories and not print out the interactions.

Try changing the first story to "can I order an espresso?" to "can I order a flat white?" and run `./run.sh rbdd flat white`. This should adjust the expected JSON.

You can hack on the .story files in story/ folder to create new scenarios and
engine.py to change the way the scenarios are executed, add new checks and more!

This test driven prompt tuning toolkit is based upon [hitchstory](https://hitchdev.com/hitchstory).

## What is in this project?

hitch/story -- contains YAML stories.

hitch/engine.py -- the execution engine for these stories. It's the director.

hitch/llm.py -- tools for the execution of OpenAI.

hitch/cli.py -- command line tools e.g. running single stories (bdd), single stories in rewrite mode (rbdd) and all stories together (regression).
