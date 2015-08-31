__author__ = 'crespowang'
from google.appengine.ext import ndb

class People(ndb.Model):
    name = ndb.StringProperty()
    position = ndb.StringProperty()
    appearance = ndb.IntegerProperty()
    twitterId = ndb.StringProperty()
    facebookId = ndb.StringProperty()
    instgramId = ndb.StringProperty()
    googleId = ndb.StringProperty()
    weiboId = ndb.StringProperty()
    wechatId = ndb.StringProperty()
    qqId = ndb.StringProperty()
    createdTime = ndb.DateTimeProperty(auto_now_add=True)


    @classmethod
    def create(cls, name, position, wechatId=None):
        people = People()
        people.populate(name=name, position=position, wechatId=wechatId)
        return people.put()

    @classmethod
    def getone(cls, id):
        return People.get_by_id(long(id))

    @classmethod
    def getall(cls):
        q = cls.query()
        return q.fetch()


