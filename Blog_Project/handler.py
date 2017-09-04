#!/usr/bin/python
import os
import jinja2
import webapp2

template_path = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_path),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.write(*args, **kwargs)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
