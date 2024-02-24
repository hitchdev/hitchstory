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

Run `./run.sh bdd flat white`

Run `./run.sh bdd pizza`

Run `./run.sh bdd cookie`

You can hack on the .story files in story/ folder to create new scenarios and
engine.py to change the way the scenarios are executed, add new checks and more!

This test driven prompt tuning toolkit is based upon [hitchstory](https://hitchdev.com/hitchstory).
