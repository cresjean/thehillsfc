__author__ = 'crespowang'
from google.appengine.ext import ndb


class Dude(ndb.Model):
    name = ndb.StringProperty()
    checkinTime = ndb.DateTimeProperty()
    wechatId = ndb.StringProperty()
    weiboId = ndb.StringProperty()
    matchId = ndb.StringProperty()
    status = ndb.StringProperty()


