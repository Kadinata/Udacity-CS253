import webapp2
from mainpage import MainPage
from rot13 import Rot13Page
from userlogin import SignupPage
from userlogin import WelcomePage
from userlogin import LoginPage
from userlogin import LogoutPage
from blog import BlogNewpost
from blog import BlogMain
from blog import BlogEntry
from blog import Flush

app = webapp2.WSGIApplication([
        ('/', MainPage),
        ('/rot13', Rot13Page),
        ('/blog/signup', SignupPage),
        ('/blog/login', LoginPage),
        ('/blog/logout', LogoutPage),
        ('/blog/welcome', WelcomePage),
        ('/blog(/\.json)?', BlogMain),
        ('/blog/(\d+)?(\.json)?', BlogEntry),
        ('/blog/newpost', BlogNewpost),
        ('/blog/flush', Flush),
    ], debug=False
)
