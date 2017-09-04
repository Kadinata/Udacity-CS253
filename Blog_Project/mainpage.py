from handler import Handler

#=================================================================
class MainPage(Handler):
    def get(self):
        self.render('mainpage.html')
#=================================================================