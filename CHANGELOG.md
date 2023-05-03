# Changelog


### 0.21.0

* FEATURE : Added cleaner exceptions for the add pytests.
* FEATURE : Helper function to turn hitchstory stories into pytest tests.


### 0.20.1

* FEATURE : Matchers have better validation.


### 0.20.0

* FEATURE : Match JSON snippets.


### 0.19.0

* FEATURE : Added convenience method to match two strings.
* FEATURE : Made hitchstory conceal useless stacktraces when running within pytest.
* BUGFIX : Raise failure if rewrite can't work.


### 0.18.0

* BUGFIX : Newer and better way to do rewriting.


### 0.17.0

* FEATURE : Run tests inside an external test runner - like pytest.


### 0.16.0

* FEATURE : Added this_step and this_story to step templates for generating documentation.


### 0.15.3

* BUGFIX : 'YAML' object has no attribute 'extend' bug.


### 0.15.2

* BUGFIX : Fixed reliance on deprecated inspect.getargspec.
* BUGFIX : Removed unnecessary dependency.
* FEATURE : Use pyproject.toml and put lower bounds on all dependency packages.
* BUGFIX : Fix story rewriting being done incorrectly when there are 'replacement steps' or 'following steps'.
* FEATURE : Readable exception for child stories that have ambiguous steps.
* FEATURE : Following / replacement steps on child stories.
* FEATURE : Clearer exceptions and storytest for invalid use of inherit_via.
* MAJOR : Backwards incompatible feature - inherit_via on given preconditions.


### 0.14.0

* FEATURE : given.child.items() usable in documentation templates.


### 0.13.3

* BUGFIX : Fix for bug caused by re-use use of with_documentation.
* BUGFIX : Failing story for re use of with_documentation.
* FEATURE : Display names properly in variation sub docs.


### 0.13.2

* FEATURE : Variations can be used to output docs.
* FEATURE : Added ability to include variation docs.
* BUGFIX : Fixed documentation error on steps with no arguments.


### 0.13.1

* FEATURE : Reference filename in story template.
* BUGFIX : Documentation templates - fix exception on info.
* FEATURE : Clearer exceptions on templates - on info.
* FEATURE : Give clean exceptions on template.
* FEATURE : Don't raise exceptions directly when coming from template.
* BUGFIX : Use given[name] in templates.
* BUGFIX : Make it possible to not take extra variables.
* FEATURE : Raise clear exception if .with_exception not used.
* FEATURE : Put variables into doc templates.
* FEATURE : Documentation generator - generate info properties.
* FEATURE : Document generation with multiple arguments in a step.
* FEATURE : Doctemplating with YAML feature.


### 0.12.1

* BUGFIX : **kwargs validators are now used correctly.


### 0.12.0

* FEATURE : Moved template documentation building of step and given snippets into engine.
* FEATURE : Highlight the word 'SUCCESS' in green on the command line.
* BUGFIX : Varargs / args exceptions are clarified so make it easier to track down the offending method.
* FEATURE : Better exception handling for given.


### 0.11.3

* BUGFIX : Fix formatting on pypi because of markdown.


### 0.11.2

* FEATURE : Raise exception if a reserved name is used for an InfoProperty.
* BUGFIX : Handle info properties which have spaces in them.


### 0.11.1

* FEATURE : Added .get() on StoryInfo objects.
* FEATURE : Added flakiness detection when single stories are run.
* FEATURE : Story files with nothing but comments are valid.
* FEATURE : When rewriting stories, doing self.new_story.rewrite() in on_success method is now unnecessary.
* FEATURE : Added .about parameter to Story object so it can be used in documentation.


### 0.10.3

* BUGFIX : Handle scenarios where step shouldn't have an argument but does.


### 0.10.2


No relevant code changes.

### 0.10.1


No relevant code changes.

### 0.10.0


No relevant code changes.

### 0.9.1


No relevant code changes.

### 0.9.0

* MAJOR REFACTOR : Removed StorySchema - now reliant upon GivenDefinition and InfoDefinition.
* MAJOR REFACTOR : Use InfoDefinition/InfoProperty instead of schema.
* MAJOR REFACTOR : Use GivenDefinition/GivenProperty instead of schema.
* MAJOR REFACTOR : Renamed expected_exception to no_stacktrace_for.


### 0.8.2


No relevant code changes.

### 0.8.1

* BUGFIX : Flush all output to stdout after it is printed.
* BUGFIX : Fixed story rewriting where arguments have underscores.
* PATCH BUGFIX : Fixed formatting on failure output.


### 0.8.0

* PATCH FEATURE : Fixed formatting of failure reports printed to screen.
* PATCH FEATURE : Prettified the failing test output.
* MAJOR FEATURE : Print report to stdout as it takes place.


### 0.7.6

* MINOR BUGFIX : Stories can do .ordered_by_file() - fix.


### 0.7.5

* MINOR FEATURE : Stories can do .ordered_by_file()


### 0.7.4

* PATCH : BUGFIX : Allow use of info parameters on variation stories.


### 0.7.3


No relevant code changes.

### 0.7.2

* PATCH : BUGFIX : Show stacktrace for set_up.
* MINOR : FEATURE : Documentation - check for properties in steps.


### 0.7.1

* PATCH : MINOR : Do nothing if story has been saved in spite of no changes being made.


### 0.7.0

* MINOR : FEATURE : Documentation.
* PATCH : REFACTOR : Renamed 'about' story.
* MAJOR : REFACTOR : Renamed 'about' to 'info'.


### 0.6.2

* PATCH : REFACTOR : Do not make copy of YAML for modifications until an update is triggered.
* MINOR : REFACTOR : Set _aborted, not aborted.
* MINOR : BUGFIX : Made series of aborted stories end when one is aborted.
* PATCH : REFACTOR : Refactored Story object.
* MINOR : FEATURE : Filter only uninherited stories.
* PATCH : REFACTOR : Cleaned up Story, Collection, StoryFile and Steps.
* MINOR : FEATURE : Filter by non-variations.


### 0.6.1

* PATCH : PERFORMANCE : Do not repeatedly reparse the YAML.
* PATCH : MINOR : Clearer exceptions for invalid YAML when running stories.
* PATCH : REFACTOR : Moved StepMethod class into its own file.
* MINOR : REFACTOR : Reworked the way arguments are passed from YAML to method.
* PATCH : REFACTOR : Clarify arguments test.
* PATCH : REFACTOR : Renamed arbitrary arguments story file to just a story about arguments.
* PATCH : BUGFIX : Run tear_down even if there is an error in on_success or on_failure.
* PATCH : REFACTOR : Refactored key.py.
* PATCH : REFACTOR : Removed unused hitchstory steps.
* PATCH : REFACTOR : Refactoring of stories along with minor code changes to make exception messages more deterministic.
* MINOR : FEATURE : all_passed property on result list.
* PATCH : REFACTOR : Moved directory getting code into utils.
* PATCH : REFACTOR : Moved more code out of story.py into a more sensible place.
* PATCH : REFACTOR : Moved StoryFile into its own file.
* PATCH : REFACTOR : Moved StoryStep into its own file.
* PATCH : REFACTOR : Removed unnecessary utils function.


### 0.6.0

* MAJOR : REFACTOR : scenario -> steps, default -> with, preconditions -> given


### 0.5.0

* MINOR : REFACTOR : Refactoring to deal with the changes introduced in the new versions of strictyaml.
* PATCH PERFORMANCE IMPROVEMENTS : Do not rerun ordered_arbitrarily code when it is called multiple times.
* PATCH : PERFORMANCE IMPROVEMENT : Speed up story loading by reducing the number of times slugify() is called.
* PATCH BUGFIX : Filtering stories restrictively broke story inheritance.
* PATCH BUGFIX : Allow use of 'default' in variations.
* PERFORMANCE : Performance improvements when parsing and building a model of stories.
* FEATURE : Added Failure exception, which is counted as an expected exception.
* FEATURE : Parameterization, defined programatically.
* FEATURE : Make parameters work solely on individual preconditions and parameters on steps.
* FEATURE : Expected exceptions in steps.


### 0.3.1

* BUGFIX : Accidental conversion to string when parameters introduced on nested structures.


### 0.3.0

* BUG : Fixed the previous inability to deal with optionals in mapping.
* BUG : Test inconsistency in continue on failure story.
* BUG : Rewriting stories did not work for variations.
* BUG : Fix strictyaml issue.
* BUG : Story rewriting did not work with strings that have more than one line.


### 0.2.9

* FEATURE : Give more details in exception about which story we are trying to inherit from is not found.
* BUG : If inherited stories are not in filtered stories, they are not runnable.


### 0.2.8

* FEATURE : Variations feature.


### 0.2.7

* FEATURE : Send result object to the on_failure method so that the result report can be printed.


### 0.2.6

* BUG : HitchStoryException was not importable from the root of the module.


### 0.2.5

* BUG : Fixed story rewriting when there is more than one keyword argument.


### 0.2.4

* FEATURE : Added __version__ variable to __init__.py, updated on deployment.
* BUG : Single variable steps not fed through the validator.


### 0.2.3

* FEATURE : Continue on failure and stop on failure.


### 0.2.2

* BUG : About schema should allow for Optionals.


### 0.2.1

* FEATURE : Type-check schema objects.
* FEATURE : Ability to let stories rewrite themselves.
* FEATURE : When invalid YAML is detected parsing a story file then the filename it occurred in is given.
* BUG : Fixed the stacktrace.
* FEATURE : Added on_abort method and trigger.
* BUG : Fixed the conversion of data fed in the parameters that have validators attached.
* FEATURE : Get story object from engine.
* FEATURE : Gradual typing on preconditions, params and steps.
* BUG : Step parameters and preconditions must not be passed to the engine method as YAML objects.
* BUG : Fixed regression caused by adding exception catching for special methods.
* FEATURE : Handle exceptions in tear_down.
* FEATURE : Handle exceptions in on_failure.
* FEATURE : Handle exception in on_success
* FEATURE : Added on_success trigger method.
* FEATURE : Added on_success.


### 0.2.0

* BUG : Precondition keys were YAML objects where they should have been strings.


### 0.1.9

* BUG : Preconditions should be strings, ints, etc. and not YAML objects.


### 0.1.8

* BUG : Preconditions should be strings, ints, etc. and not YAML objects.


### 0.1.7

* FEATURE : Handle invalid story collection parameters more cleanly.


### 0.1.6

* FEATURE : Display correct tracebacks upon failure.


### 0.1.5

* FEATURE : Story with arbitrary number of arguments.


### 0.1.4

* FEATURE : Hide hitchstory framework code from stacktraces that are displayed upon exceptions.
* FEATURE : Added YAML steps to failure reports.
* BUG : Fixed breakage of regular tests without added properties.
* BUG : Fixed inheritance issue.
* FEATURE : Added prettystack.


### 0.1.3

* FEATURE : List multiple matching stories.


### 0.1.2


No relevant code changes.
