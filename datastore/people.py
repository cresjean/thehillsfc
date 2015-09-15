__author__ = 'crespowang'
from google.appengine.ext import ndb
from hashlib import sha256
from random import random
import base64


class People(ndb.Model):
    name = ndb.StringProperty()
    username = ndb.StringProperty()
    position = ndb.StringProperty()
    appearance = ndb.IntegerProperty()
    twitterId = ndb.StringProperty()
    facebookId = ndb.StringProperty()
    instgramId = ndb.StringProperty()
    googleId = ndb.StringProperty()
    weiboId = ndb.StringProperty()
    wechatId = ndb.StringProperty()
    qqId = ndb.StringProperty()
    passwordseed = ndb.FloatProperty()
    password = ndb.StringProperty()
    admin = ndb.BooleanProperty(default=False)
    createdTime = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create(cls, name, username):
        people = People()
        people.populate(name=name, username=username)
        return people.put()

    @classmethod
    def getbyusername(cls, username):
        q = cls.query(cls.username == username)
        return q.get()


    @classmethod
    def getone(cls, id):
        return People.get_by_id(long(id))

    @classmethod
    def getall(cls):
        q = cls.query()
        return q.fetch()

    def genpass(self, password):

        seed = random()
        pwd = base64.b64encode(sha256("{}{}{}".format("paqwe1e!#", seed, password)).digest()).decode()
        self.passwordseed = seed
        self.password = pwd
        self.put()

    def validpassword(self, password):
        pwd = base64.b64encode(sha256("{}{}{}".format("paqwe1e!#", self.passwordseed, password)).digest()).decode()
        if pwd == self.password:
            return True
        else:
            return False



