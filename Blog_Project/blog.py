#!/usr/bin/python
from google.appengine.api import memcache
from google.appengine.ext import db
from bloghandler import BlogHandler, Handler
from dbschema import Blog
import time

#=================================================================
class BlogParent(BlogHandler):

    def get_post_by_id(self, post_id, update=False):
        if post_id and post_id.isdigit():
            cache_key = post_id
            post = memcache.get(cache_key)
            if post is None or update:
                post_key = db.Key.from_path('Blog', int(post_id))
                post = db.get(post_key)
                if not post:
                    return (None, None)
                post = (post, time.time())
                memcache.set(cache_key, post)
            return post
        return (None, None)

    def top_posts(self, update = False):
        key = 'front'
        posts = memcache.get(key)
        if (posts is None) or update:
            posts = Blog.all().order('-created').fetch(limit=10)
            posts = (list(posts), time.time())
            memcache.set(key, posts)
        return posts

    def render_posts(self, posts, age):
        self.render('blog_main.html', blogposts=posts, age=age)

#=================================================================
class BlogMain(BlogParent):
    def get(self, json_mode=False):
        posts, timestamp = self.top_posts()
        if self.format == 'json':
            self.render_json([p.as_dict() for p in posts])
            return
        age = int(time.time() - timestamp)
        self.render_posts(posts, age)

#=================================================================
class BlogEntry(BlogParent):
    def get(self, blog_id, json_mode=False):
        post, timestamp = self.get_post_by_id(blog_id)
        if not post:
            self.error(404)
            return
        if self.format == 'json':
            self.render_json(post.as_dict())
            return
        age = int(time.time() - timestamp)
        self.render_posts([post], age)

#=================================================================
class BlogNewpost(BlogParent):

    def render_main(self, subject="", content="", error=""):
        self.render(
            'blog_newpost.html',
            subject=subject,
            content=content,
            error=error
        )

    def get(self):
        if not self.user:
            self.redirect('/blog/login')
            return
        self.render_main()

    def post(self):
        if not self.user:
            self.redirect('/blog/login')
            return
        subject = self.request.get("subject")
        content = self.request.get("content")
        error = ""
        if subject and content:
            if len(subject) > 50:
                error = "Subject line is too long."
                self.render_main(subject, content, error)
                return
            blog = Blog(subject = subject, content = content)
            blog.put()
            self.top_posts(True)
            self.redirect("/blog/{0}".format(blog.key().id()))
        elif not (subject or content):
            error = "Subject and content must not be empty."
        elif not subject:
            error = "Please enter a subject line."
        elif not content:
            error = "Please enter blog content."            
        self.render_main(subject, content, error)
        
#=================================================================
class Flush(Handler):
    def get(self):
        memcache.flush_all()
        self.redirect('/blog')
#=================================================================