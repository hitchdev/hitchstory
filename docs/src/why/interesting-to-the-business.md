---
title: Why does hitchstory not have an opinion on what counts as interesting to "the business"?
---

When Cucumber first gained some popularity, there was something of a backlash
from the original developers that the users "[weren't using it correctly](https://cucumber.io/blog/collaboration/the-worlds-most-misunderstood-collaboration-tool/)":

The specific complaint was that it was being used as an integration testing
framework rather than a tool for "communicating with the business" and that everything
except the high level "business requirements" should be abstracted away.

Hitchstory takes a different approach and recommends using it as an integration testing framework *primarily* and use [documentation generation tools](../../using/documentation/generate) to produce documentation from that, where necessary, that is of an appropriate level of detail for stakeholders.

This is because:

- "The business", from a BDD perspective, is a hypothetical entity which does not really exist. There are different kinds of stakeholders - lots of different people who have varying levels of interest in the different parts of the specification.

- Stakeholders rarely have any interest in implementation details and only have an interest in some aspects of the specification.

3. Stakeholder interest in the details of your software's behavior will vary wildly. Sometimes they will want only vague details, other times they will be interested in obscure business logic, and other times they will be interested in specific user UI actions.

4. Interest varies from stakeholder to stakeholder - UX designers, UI designers, translators, product managers and the CEO will all have varying levels of interest in the specifics of the behavior of your software.

5. The language that is most appropriate for specifying code is not necessarily going to be English or English-like. 

Nonetheless, despite all of this, the Cucumber people were on to something - there is a tight relationship between documentation and specification.

HitchStory takes the view that all behavior should be specified by a user story, along with any appropriate metadata and that documentation should be generated.
