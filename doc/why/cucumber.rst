Why not use Cucumber or other Gherkin-derived languages?
========================================================

Original : Cucumber
Python equivalents: lettuce, behave.
Java equivalent: JBehave

Gherkin was not a clearly designed language which even the language
designer admitted to. It was more of an idea about
development that was put forward and then cobbled together.

Unfortunately, because of this, the syntax is both ambiguous and verbose, which
is why gherkin derived languages suffer from the following issues:


Regular expressions
-------------------

   [ JAMIE ZAWINKSKI QUOTE ]

The use of regular expressions in cucumber was done as a hack to enable the use of
"English-like" sentences in the construction of user stories.

There are a multiplicity of examples around the web where it went wrong causing headaches
for users.

http://coryschires.com/ten-tips-for-writing-better-cucumber-steps/


The need to use multiple parsers and have the story writer "choose" which one to use
------------------------------------------------------------------------------------

This is in evidence in lettuce. [ MORE EXPLANATION ]


Verbosity
---------

The stories are much longer than they need to be.


A lack of inheritance
---------------------

