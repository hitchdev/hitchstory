# REST API Tests with Pytest, HitchStory and Podman

<div align="center">
  <div style="display: flex;">
    <img src="https://hitchdev.com/images/rest-api-story.png" style="vertical-align: top;" />
    <img src="https://hitchdev.com/images/rest-api-docs.png" />
  </div>
</div>

This example project demonstrates a combination of best practices and state of the art practices for isolated REST API tests:

* One step set up: ./run.sh make.
* Absolute and total environmental consistency and portability (Mac/WSL/Linux) via containerization and dependency pinning.
* Every project task runnable via one script (./run.sh) - building, running tests, generating docs, re-pinning dependencies.
* The handling of fields whose outputs vary upon each test run (UUID, timestamp).
* Rewritable stories: if the REST API response is modified in code, running the test in rewrite mode will rewrite the response in the test.
* Rewritable documentation: templated generation of readable markdown docs demonstrating user stories with API snippets (useful for BDD).
* Ultra simple 3 step github actions config to run all of the tests.

It is a work in progress. These are some features I'll be adding soon:

- [ ] Database fixtures - similar to how it works in the website example https://github.com/hitchdev/hitchstory/blob/master/examples/website/
- [ ] Use of podman-compose - similiar to https://github.com/hitchdev/hitchstory/blob/master/examples/website/
- [ ] Validation of UUID and timestamp (e.g. via regex).

## Set up

**Podman must be installed on your system first.**

All other functionality is automated and can be run via one of the 
four run.sh scripts.

To begin:

```bash
$ git clone https://github.com/hitchdev/hitchstory.git
$ cd hitchstory/examples/restapi
$ ./run.sh make  # builds one local container and volume, and one container inside it
```



## Clean up everything

Everything runs in one podman container and volume. This deletes them:

```
$ ./run.sh clean all
```

# Github Actions

These integration tests are run via github actions on every push (along with the tests for 3 other projects). The steps are kept deliberately
simple to prevent a CI debugging explosion.

* [Github actions YAML](https://github.com/hitchdev/hitchstory/blob/master/.github/workflows/examples.yml)
* [Runner](https://github.com/hitchdev/hitchstory/actions/workflows/examples.yml)

# Architecture

The tests in this project are run from a podman container and the REST API is run in a container run *inside* that container:

```mermaid
graph TD;
    TestContainer-->AppContainer;
```
