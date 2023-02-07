---
title: How can executable specifications and living documentation be used for stakeholder collaboration?
---

A while back while I was still trialing this framework I received an enormous JIRA ticket
describing the complex logic flows and behavior of a command line application.

This was bad enough The worst part, though, was that I actually didn't *really*
understand what I was building.

## Collaborating with an executable specification

Gradually I turned those descriptions in to an executable specification that described how
the command line tool was supposed to behave. That meant writing a series of YAML stories
that said "if the app was run with abc parameters then it should do xyz, etc."

I built executable hitchstory specs that I thought described about
90% what the product manager wanted - there were still critical pieces missing.

The translation process was not easy because the Jira ticket was often vague
because the descriptions were sometimes vague, always complicated and
occasionally missing key nuggets of information.

The "magic" happened when I showed the YAML specifications to him. He was instantly able
to identify the behavior I had inferred from his JIRA ticket and not only
the correct the mistakes that I'd made interpreting him, but also mistakes *he'd* made
*writing* the ticket - just by looking over my shoulder.

At the same time as correcting my mistakes I tried noting down metadata
[alongside the stories](../../using/metadata) - about *why* the behavior
was as it was although due to time pressures I never really did figure it out
and document it.

## Writing the code

As I wrote the specifications and implemented the code new scenarios that weren't
obvious before suddenly became obvious. Each time either asked him what the behavior
should be and wrote it up or just wrote it up (if it seemed fairly obvious).

Whether it was obvious or not, however, I still circled round and double checked
the desired behavior with executable stories precisely because what I thought was
obvious could have been wrong and what I heard verbally or via chat I might not have
interpreted accurately.

Indeed, this was exactly the case - I did misinterpret him and I did make faulty
assumptions.

In all cases, having a highly specific spec following the [screenplay principle](../screenplay-principle)
to refer to gave us both the confidence that I was building the right thing.

## Wherein the code rewrites the story

Since it was a command line application I was building, the nature of the
stories followed a basic pattern:

* Run command with parameters a, b, c
* The command calls a mock database (and the call needs to be verified).
* The command outputs on to the screen.

Now, I could have done the strictest form of TDD where I wrote the test/spec
first *always* and then wrote the code that made it pass.

Instead, I opted for a looser approach. I wrote the basic outline of the
test first, *then* I wrote the code and *then* I ran the test in [rewrite
mode](../../using/rewrite-story) so that whatever the command line output
was, that was written directly in to the story automatically if the rest of
the scenario didn't fail.

Then I reloaded the story in the text editor and eyeballed it to see that it
looked correct.

*Then* I circled back to the product owner and verified that the whole story
looked correct together.

This had all of the benefit of test driven development except it cut the
amount of time required to write the story in half.


## Aftermath

QA picked up bugs afterwards when integration testing, but surprisingly, 
they were all either mistakes the product manager had made himself or
environment issues. The logic of the program wasn't extremely complicated
so this wasn't a gratitously monumental achievment but it was still cool.

The *shocking* part was that by using hitchstory and following the process of
iterating jointly with the product manager I managed to build an entire software
system with the *barest* domain knowledge and no real understanding of why it did
what it did.

And it worked.

And I still don't really understand why it did what it did.
