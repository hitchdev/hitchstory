class Webdriver(object):
    def __init__(self, name=None, platform=None, version=None, dimensions=None):
        if name is not None:
            print("\nBrowser name: {}".format(name))
        if platform is not None:
            print("Platform: {}".format(platform))
        if version is not None:
            print("Version: {}".format(version))
        if dimensions is not None:
            print("Dimensions: {height} x {width}".format(**dimensions))

    def visit(self, website):
        print("\nVisiting {}".format(website))

    def fill_form(self, name, content):
        if '\n' in content:
            print("In {} entering text:\n{}\n".format(name, content))
        else:
            print("Entering text {} in {}".format(content, name))

    def click(self, name):
        print("Clicking on {}".format(name))
