HitchStory
==========

HitchStory is a python library for running executable specifications.

Storyfile is a YAML based DSL for writing `BDD <https://en.wikipedia.org/wiki/Behavior-driven_development>`_-style
executable user stories for any kind of software.

Dogfooded for *years* on high and low level software.

The stories are designed to be:

* Readable
* Declarative
* DRY as sand
* Strongly typed and syntactically sound `StrictYAML <https://github.com/crdoconnor/strictyaml>`_
* Parameterized and useable with `hypothesis <http://hypothesis.works>`_ to do property based testing.
* Self rewriting (without magic)
* Used to generate pretty documentation for users, stakeholders, translators, managers, etc.
* 100% buzzword compliant.

Hate writing tests? Hate writing documentation? Made to feel guilty about it?

Prefer writing specifications?

Yeah, me too.

Note
----

It is currently in ALPHA. APIs may change without warning until version >= 1.0.

Only runs in python 3, but still able to test python 2 code.

Example
-------

email.story:

.. code-block:: yaml

  Log in:
    given:
      website: /login                # preconditions
    steps:
      - Fill form:
          username: (( name ))       # parameterized steps
          password: (( password ))
      - Click: login
    with:
      name: AzureDiamond             # default parameters for story
      password: hunter2

  
  Send email:
    based on: log in                 # continues from test above
    steps:
      - Click: new email
      - Fill form:                   
          to: Cthon98@aol.com
          contents: |                # long form text
            Hey guys,
            
            I think I got hacked!
      - Click: send email
      - Email was sent

Corresponding python story engine and runner code:

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

  StoryCollection(["email.story"], Engine()).named("Send email").play()



Install
-------

To install::

  $ pip install hitchstory


Why not X instead?
------------------

Since hitchstory is, in some sense, a reinvented wheel, some justification is needed (TODO):

* Why not just write unit tests (e.g with py.test)?
* Why not use Cucumber / Behat / Lettuce / pytest-bdd?
* Why not use mamba / flowp?
* Why not use robot framework?
