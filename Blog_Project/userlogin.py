#!/usr/bin/python
from bloghandler import BlogHandler
from dbschema import User
import re

#=================================================================
RE_UNAME = re.compile('^[a-zA-Z0-9_-]{3,20}$')
RE_PASSW = re.compile('^.{3,20}$')
RE_EMAIL = re.compile('^[\S]+@[\S]+\.[\S]+$')

#=================================================================
def valid_username(username):
    return username and bool(RE_UNAME.match(username))

def valid_password(password):
    return password and bool(RE_PASSW.match(password))

def valid_email(email):
    return (not email) or bool(RE_EMAIL.match(email))

#=================================================================
class SignupPage(BlogHandler):

    def render_main(self, **kw):
        self.render('signup.html', **kw)
    
    def get(self):
        self.render_main()

    def post(self):
        err_uname  = ""
        err_passw  = ""
        err_verify = ""
        err_email  = ""
        
        uname  = self.request.get('username')
        passw  = self.request.get('password')
        verify = self.request.get('verify')
        email  = self.request.get('email')

        if (valid_username(uname) and valid_password(passw) and (passw == verify) and valid_email(email)):

            # Verify user does not already exist
            if not User.by_name(uname):
                
                # create password hash and salt
                new_user = User.register(uname, passw, email)
                new_user.put()
                self.login(new_user)
                self.redirect('/blog/welcome')
                return
            else:
                err_uname = "Username is already used."

        if not valid_username(uname):
            err_uname = "Username is not valid."

        if not valid_password(passw):
            err_passw = "Password is not valid."

        if (passw != verify):
            err_verify = "Passwords did not match."

        if not valid_email(email):
            err_email = "Email address is not valid."

        self.render_main(
            uname = uname,
            email = email,
            err_uname = err_uname,
            err_passw = err_passw,
            err_verify = err_verify,
            err_email = err_email,
        )

#=================================================================
class WelcomePage(BlogHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', uname=self.user.username)
        else:
            self.redirect('/blog/signup')

    def post(self):
        self.redirect('/blog/logout')

#=================================================================
class LoginPage(BlogHandler):
    
    def render_main(self, error=""):
        self.render('login.html', error=error)
    
    def get(self):
        self.render_main()

    def post(self):
        uname  = self.request.get('username')
        passw  = self.request.get('password')
        user = User.login(uname, passw)
        if user:
            self.login(user)
            self.redirect('/blog/welcome')
            return

        self.render_main(error = 'Invalid username or password')

#=================================================================
class LogoutPage(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog/signup')

#=================================================================