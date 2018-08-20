I am perfectly happy with py.test (or other unit testing framework). Why should I use hitchstory?
-------------------------------------------------------------------------------------------------

Ultimately it boils down to two programming principles which hitchstory does not strictly enforce,
but *does* guide you to follow via its design:

* The rule of least power
* Separation of concerns

Hitchstory stories describe a sequence of events which describe either a user or a user-system
interacting with your code. This can be used to describe the functioning of any software system.
It is not necessary** to use turing complete code to describe a sequence of events, therefore,
according to the rule of least power, you shouldn't use turing complete code to do it.

However, turing complete code *is* required to set up and mimic this set of events. This is
what the hitchstory engine is used for, which must be written in turing complete python.

This divide between story definition and story execution also creates a natural barrier for the
separation of concerns. Story definition goes in the stories while execution goes in the engine.
Unit testing frameworks do not have any such natural barrier for separation of concerns.

Web developers may be familiar with this principle as it is expressed in web development
frameworks where (intentionally less powerful) templating languages are used to render HTML,
separated by a divide from more powerful 'controller' (or, in Django, 'view') code.

Other features which are not (and cannot) be duplicated in unit testing frameworks:

* Automated story modification

The hitchdev framework does come with a lot of useful testing tools which could just as
easily be used with py.test if you so wish.
