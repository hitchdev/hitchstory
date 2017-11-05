HitchStory
==========

HitchStory is a python library for running executable specifications.

Storyfile is a YAML based DSL for writing BDD-style executable user stories.
It can be used for writing executable specifications and tests at any
level of the testing pyramid.

It is currently in ALPHA. APIs may change without warning until version >= 1.0.

Example
-------

login.story:

.. code-block:: yaml

  # All about the character
  Log in as John:
    given:
      website: /login
    steps:
    - Fill form:
        username: john
        password: hunter2
    - Click: login

Corresponding python story engine and runner code:

.. code-block:: python

  from hitchstory import BaseEngine, StoryCollection
  from tellurium import CyberDriver
  
  class Engine(BaseEngine):
      def set_up(self):
          self.driver = CyberDriver()
          self.driver.visit(
              "http://localhost:5000{0}".format(self.given['website'])
          )

      def fill_form(self, **textboxes):
          for name, contents in textboxes.items():
              self.driver.fill_form(name, contents)
      
      def click(self, name):
          self.driver.click(name)

  StoryCollection(["login.story"], Engine()).one().play()


StoryFile Features
------------------

* Declarative - why user stories are better when declarative than turing complete?
* Terse - syntactically designed to minimize specification code with no loss of expressiveness.
* Type-safe - strongly typed preconditions, metadata and step arguments using StrictYAML (optional).
* Story inheritance - keep your stories meaningful, specific *and* DRY.
* Parameterization - for easy property testing.

HitchStory Features
-------------------

* Automated documentation generation - keep your documentation, specification and testing in sync by deriving them from a single source of truth.
* Automated story rewriting - include story artefacts (e.g. command line output) as part of your test and rewrite them automatically when changed.
* Documented extensively with real life examples.
* Customizable story metadata - for easy addition of tags, JIRAs, etc. to stories.
* Extensively dogfooded


Install
-------

To install::

  $ pip install hitchstory


Why not X instead?
------------------

Since hitchstory is a reinvented wheel, justification is needed:

* Why not just write unit tests (e.g with py.test)?
* Why not use Cucumber / Behat / Lettuce / pytest-bdd?
* Why not use mamba / flowp?
* Why not use robot framework?
