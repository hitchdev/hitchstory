# HitchStory REST API Tests Example

## Run them yourself

**Podman must be installed on your system first.**

All other functionality is automated and can be run via one of the 
four run.sh scripts.

To begin:

```bash
$ git clone https://github.com/hitchdev/hitchstory.git
$ cd hitchstory/examples/restapi
$ ./run.sh make
```

`./run.sh make` downloads and builds the container and python packages the
tests need to run in an isolated environment for each of the respective projects.


## Run all tests

```
$ ./run.sh regression
```

## Run a single test

This command can be used to craft a new feature and do
acceptance test driven development on it:

```
$ ./run.sh atdd correct
```

"correct" is a unique keyword used in the name of one of the stories.

## Run singular test in rewrite mode

If you tweak the wordings in the command line app and run this, it will
update the story accordingly.

```
$ ./run.sh ratdd correct
```

## Generate documentation from stories

This will regenerate all of the markdown docs for the project:

```
$ ./run.sh docgen
```

## Clean up everything

When ./run.sh make is run on any of these 4 project, it will create one podman image and one volume
each. This command cleans them both up:

```
$ ./run.sh clean all
```
