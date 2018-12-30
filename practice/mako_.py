
from mako.template import Template
from os.path import dirname, abspath
from nanohttp import Controller, html, Static


class Root(Controller):
    static = Static(abspath(dirname(__file__)))

    @html
    def index(self):
        mytemplate = Template(filename='a.mako')
        return mytemplate.render(items=[1, 2, 3, 4, 5, 6])


