HitchStory
==========

HitchStory is a python 3 library for building BDD-style executable specifications.

It is currently in ALPHA. APIs may change without warning until version >= 1.0.

Example
-------

email.story:

.. code-block:: yaml

  Log in:
    with:
      name: AzureDiamond             # default parameters for story
      password: hunter2
    given:
      website: /login                # preconditions
    steps:
      - Fill form:
          username: (( name ))       # parameterized steps
          password: (( password ))
      - Click: login

  
  Send email:
    based on: log in                 # inherits from and continues from test above
    steps:
      - Click: new email
      - Fill form:                   
          to: Cthon98@aol.com
          contents: |                # long form text
            Hey guys,
            
            I think I got hacked!
      - Click: send email
      - Email was sent

Corresponding python execution engine:

.. code-block:: python

  from hitchstory import BaseEngine, StoryCollection
  from tellurium import CyberDriver
  from emailchecker import email_was_sent
  
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
      
      def email_was_sent(self):
          email_was_sent()

This runs the story:

.. code-block:: python

    >>> StoryCollection(["email.story"], Engine()).named("Send email").play()

Install
-------

To install::

  $ pip install hitchstory


Tell me more
------------

HitchStory is a YAML based DSL for writing stories that is designed primarily to be ergonomic
for developers and only *incidentally* "`business readable <https://www.martinfowler.com/bliki/BusinessReadableDSL.html>`_".

By ergonomic for programmers, I mean:

* Stories can *and should* inherit from one another, because *specifications ought to be DRY too*.
* Stories are defined and validated using strongly typed StrictYAML. Step arguments and preconditions ('given') schemas can be defined by the programmer.
* The execution engine can be programmed to rewrite the executing story based upon program behavior changes (e.g. screen output changes, labels on a web app change).
* Running stories is done via a python API so you can easily write customized test workflows to suit your workflows.
* Story parameterization is built in.

This library was dogfooded for years to BDD, test and autodocument a variety
of different kinds of software - web apps, python libraries, command line apps.
  
  
Why not X instead?
------------------

* Why not just write unit tests (e.g with py.test)?
* Why not use Cucumber / Behat / Lettuce / pytest-bdd?
* Why not use robot framework?
