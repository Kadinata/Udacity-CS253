#!/usr/bin/python
from handler import Handler

#=================================================================
class Rot13Page(Handler):

    def render_main(self, text=""):
        self.render('rot13.html', text=text)

    def get(self):
        self.render_main()

    def post(self):
        encoded = ''
        text = self.request.get('text')
        if text:
            encoded = text.encode('rot13')
        self.render_main(encoded)
#=================================================================