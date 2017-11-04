HitchStory
==========

HitchStory is a python libary for validating and executing storyfiles.

Storyfile is a YAML based DSL for writing BDD-style executable user stories.
It can be used for writing executable specifications and tests on any
level of the pyramid.

It is currently in ALPHA. APIs may change without warning until version >= 1.0.

Example
-------

login.yaml:

.. code-block:: yaml

  # All about the character
  Log in as John:
    given:
      website: www.supersecretsite.com/login
    steps:
    - Fill form:
        username: john
        password: hunter2
    - Click: login

Engine:

.. code-block:: python

  from hitchstory import BaseEngine, StoryCollection
  from tellurium import CyberDriver
  
  class Engine(BaseEngine):
      def set_up(self):
          self.driver = CyberDriver()
          self.driver.visit(self.given['website'])

      def fill_form(self, **textboxes):
          for name, contents in textboxes.items():
              self.driver.fill_form(name, contents)
      
      def click(self, name):
          self.driver.click(name)

  StoryCollection(["login.story"], Engine())\
      .ordered_by_name()
      .one()
      .play()


Features
--------

* Automated documentation generation
* Automated story rewriting
* Story inheritance
* Optionally type-safe
* Parameterization
* Extensively dogfooded


Install
-------

To install::

  $ pip install hitchstory


Why not X?
----------

* Why not use Cucumber / Behat?
* Why not use py.test?
* Why not use robot framework?
