Where Gherkin went wrong again: What counts as interesting to "the business"?
=============================================================================

When Cucumber first gained some popularity, there was something of a backlash
from the original developers that the users "weren't using it correctly":


The specific complaint was that it was being used as an integration testing
framework rather than a tool for "communicating with the business".

There are several things wrong with this:

#1 There really isn't any "the business", there are just stakeholders - lots of different people are interested in the behavior of the software.

#2 Stakeholders rarely have an interest in the implementation details, but they are always concerned with the behavior of software - nonetheless, the level of detail which they are interested in will vary widely.

#3 Even individual interest in behavioral details can vary over time - sometimes they will want only vague details, other times they will be interested in obscure business logic, and other times they will be interested in specific user UI actions.

#4 There is no "one true language" which can be used to communicate on a level that both stakeholders and developers can agree on.

#5 The language that is most appropriate for specifying code is not going to be the representation that is easiest for stakeholders to understand.

#6 A representation that suits one stakeholder will not necessarily suit another.

#7 Representations should be generateable from the code specification language.

