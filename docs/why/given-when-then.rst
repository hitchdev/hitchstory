I see given but where is when and then?
---------------------------------------

You can certainly write user stories using when and then like so:

  Given:
    I have: red box
  Steps:
    - When I click: the red button
    - Then it goes kaboom
  
However, I believe strongly that terseness, when it does not inhibit understanding, is a key
principle of good programming.

Writing the story like this is shorter and is, in my opinion, exactly as clear:

  given:
    box: red
  steps:
    - click: red button
    - goes kaboom
