Invalid type in step:
  preconditions:
    files:
      example.story: |
        Create files:
          scenario:
            - Add product:
                name: Towel
                quantity: Three
  scenario:
    - Run command: |
        from hitchstory import StoryCollection, BaseEngine, validate
        from strictyaml import Int
        from pathquery import pathq


        class Engine(BaseEngine):
            @validate(quantity=Int())
            def add_product(self, name, quantity):
                pass


        result = StoryCollection(pathq(".").ext("story"), Engine()).one().play()
        output(result.report())
    - Output contains: found non-integer


Invalid validator on step:
  preconditions:
    files:
      example.story: |
        Create files:
          scenario:
            - Add product:
                name: Towel
                quantity: Three
  scenario:
    - Assert exception: 
        command: |
          from hitchstory import StoryCollection, BaseEngine, validate
          from strictyaml import Int
          from pathquery import pathq


          class Engine(BaseEngine):
              @validate(not_an_argument=Int())
              def add_product(self, name, quantity):
                  pass


          result = StoryCollection(pathq(".").ext("story"), Engine()).one().play()
          output(result.report())
        exception: StepContainsInvalidValidator



Callable step not found:
  preconditions:
    files:
      example.story: |
        Create files:
          scenario:
            - Add product:
                name: Towel
                quantity: Three
  scenario:
    - Run command: |
        from hitchstory import StoryCollection, BaseEngine
        from pathquery import pathq


        class Engine(BaseEngine):
            def set_up(self):
                self.add_product = 1

            def tear_down(self):
                pass

        result = StoryCollection(pathq(".").ext("story"), Engine()).one().play()
        output(result.report())
    - Output contains: StepNotCallable


Method not found:
  preconditions:
    files:
      example.story: |
        Create files:
          scenario:
            - Add product:
                name: Towel
                quantity: Three
  scenario:
    - Run command: |
        from hitchstory import StoryCollection, BaseEngine
        from pathquery import pathq


        class Engine(BaseEngine):
            def set_up(self):
                pass

            def tear_down(self):
                pass

        result = StoryCollection(pathq(".").ext("story"), Engine()).one().play()
        output(result.report())
    - Output contains: StepNotFound
