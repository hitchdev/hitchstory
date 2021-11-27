---
title: Why does hitchstory not have an opinion on what counts as interesting to "the business"?
---

When Cucumber first gained some popularity, there was something of a backlash
from the original developers that the users "weren't using it correctly":

The specific complaint was that it was being used as an integration testing
framework rather than a tool for "communicating with the business" and that everything
except the high level "business requirements" should be abstracted away.

Hitchstory takes a different approach and recommends the [screenplay principle](../../approach/screenplay-principle)
instead, for the following reasons:

1. "The business", from a BDD perspective, is a hypothetical entity which does not really exist. There are just stakeholders - lots of different people who are interested in your software with who you need to communicate *about* the software.

2. Stakeholders rarely have any interest in the implementation details, but they are interested in the behavior of the software.

3. Stakeholder interest in the details of your software's behavior will vary wildly. Sometimes they will want only vague details, other times they will be interested in obscure business logic, and other times they will be interested in specific user UI actions.

4. Interest varies from stakeholder to stakeholder - UX designers, UI designers, translators, product managers and the CEO will all have varying levels of interest in the specifics of the behavior of your software.

5. The language that is most appropriate for specifying code is not necessarily going to be English or English-like. 

Nonetheless, despite all of this, the Cucumber people were on to something - there is a close relationship
between documentation and specification.

HitchStory takes the view that all behavior should be specified by a user story, along with any appropriate metadata. It takes the 
approach that documentation that is fit for stakeholders should be *generated* and the specifics and the levels of detail in that
documentation should be up to the developer.
