class Webdriver(object):
    def visit(self, website):
        print("\nVisiting {}".format(website))

    def fill_form(self, name, content):
        if '\n' in content:
            print("In {} entering text:\n{}\n".format(name, content))
        else:
            print("Entering text {} in {}".format(content, name))

    def click(self, name):
        print("Clicking on {}".format(name))
