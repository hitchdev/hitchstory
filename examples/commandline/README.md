# HitchStory Command Line Tests Example

## Run them yourself

**Podman must be installed on your system first.**

All other functionality is automated and can be run via one of the 
four run.sh scripts.

To begin:

```bash
$ git clone https://github.com/hitchdev/hitchstory.git
$ cd hitchstory/examples/commandline
$ ./run.sh make
```

`./run.sh make` downloads and builds the container and python packages the
tests need to run in an isolated environment for each of the respective projects.


## Run all tests

```
$ ./run.sh pytest
```

## Run a single test

This runs "Add and retrieve todo" from `story/add-todo.story`:

```
$ ./run.sh pytest -k test_add_and_retrieve_todo
```

"correct" is a unique keyword used in the name of one of the stories.

## Run singular test in rewrite mode

If you tweak the wordings in the command line app and run this, it will
update the story:

```
$ STORYMODE=rewrite ./run.sh pytest -k test_add_and_retrieve_todo
```

## Generate documentation from stories

This will regenerate all of the markdown docs for the project:

```
$ ./run.sh docgen
```

## Clean up everything

When ./run.sh make is run, it will create one podman image and volume. This command cleans them both up:

```
$ ./run.sh clean all
```
