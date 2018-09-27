---
title: Does hitchstory let your BA or Product Manager write stories while you just write the code?
---

No. Having "analysts" write stories instead of programmers is an explicit
non-goal, unlike that of Cucumber. Well maintained stories require the eye
of a programmer - to ensure they are DRY and to maintain a proper separation
of concerns between implementation and specification.

It ought to be *possible* to write hitch stories with less training than is required
to be a programmer since the language is conceptually simpler than turing complete
programming languages. Nonetheless, it's better to write it together than to have
either the programmer or the BA write the story.

Where your BA/PO/PM is *completely* uninterested in hitchstory, it should still be
possible to use it as an effective tool of specification and test just for developers.
