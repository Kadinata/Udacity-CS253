from handler import Handler
from dbschema import User
import crypto
import json

class BlogHandler(Handler):

    def set_secure_cookie(self, key, value):
        cookie_value = crypto.secure_mesg(value)
        self.response.headers.add_header(
            'Set-Cookie',
            '{0}={1}; Path=/'.format(key, cookie_value)
        )

    def read_secure_cookie(self, key):
        cookie_value = self.request.cookies.get(key)
        return cookie_value and crypto.validate(cookie_value)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        Handler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
        self.format = 'html'
        if self.request.url.endswith('.json'):
            self.format = 'json'

    def render_json(self, d):
        self.response.content_type = 'application/json; charset=UTF-8'
        self.response.write(json.dumps(d))