---
title: Can I do BDD with hitchstory? How do I do BDD with hitchstory? 
---

Short answer: yes, but you can also do BDD with a pencil and a napkin.

The time when it was most useful as a “BDD tool” was when I was working with an extremely technical product manager who was proposing behavior in a command line tool he wanted.

Initially I received a word document describing the complex logic flows and behavior which he wanted. Gradually I turned those descriptions in to HitchStory specifications that described how the command line tool was supposed to behave. This was a process fraught with difficulty because the descriptions were often vague, complicated, overloaded and missing data. Worse, I actually didn’t really understand what I was building.

I built executable hitchstory specs that I thought were 95% what the product manager wanted.

I then showed the HitchStory specs to the product manager and explained what they meant. Because he could understand the specs he could correct the mistakes I’d made interpreting the original requirements just by looking over my shoulder and also explain why the command line tool was supposed to behave in those ways.

At the same time as correcting my mistakes I noted down alongside the stories why each behavior was necessary.

Once I he told me that I’d interpreted him correctly by reading my specs I could start writing the code.

QA picked up bugs afterwards but they were all either (quickly rectified) mistakes he’d made himself in the spec or environment issues. Surprisingly, I had zero spec<->programmer communication issues even though the domain was very complex and I still didn’t understand it.

Gherkin could have been used to do this in theory, but in practice the spec is not sufficiently expressive and the stories would have ended up being unusably vague. Unit tests could also do this in theory I guess, but good luck getting a stakeholder to read them.
