#!/usr/bin/python
from google.appengine.ext import db
import crypto
import time

TIME_FORMAT = "%a %b %d %H:%M:%S %Y"

#=================================================================
class Blog(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    def as_dict(self):
        return {
            'subject': self.subject,
            'content': self.content,
            'created': self.created.strftime(TIME_FORMAT),
        }

#=================================================================
class User(db.Model):
    username  = db.StringProperty(required=True)
    passwhash = db.StringProperty(required=True)
    passwsalt = db.StringProperty(required=True)
    email     = db.StringProperty()
    created   = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def by_name(cls, username):
        return cls.all().filter('username =', username).get()

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid)

    @classmethod
    def register(cls, username, password, email=None):
        pw_hash, salt = crypto.hash_password(username, password)
        return User(
            username  = username,
            passwhash = pw_hash,
            passwsalt = salt,
            email = db.Email(email if email else 'None')
        )

    @classmethod
    def login(cls, username, password):
        user = cls.by_name(username)
        if user and crypto.verify_password(username, password, user.passwsalt, user.passwhash):
            return user

#=================================================================