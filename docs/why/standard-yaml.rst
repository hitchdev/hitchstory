Why did you not use standard YAML for hitch?
--------------------------------------------

hitchtest (the precursor to hitchstory) actually did use standard YAML and the more I used it the
more convinced I was that it contained serious flaws. I wrote StrictYAML, which is a restricted
subset of standard YAML, in response to those flaws. It replaces implicit typing with strong typing
and deactivates rarely used and confusing YAML features.
