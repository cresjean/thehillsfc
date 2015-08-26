__author__ = 'crespowang'
from google.appengine.ext import ndb

class People(ndb.Model):
    name = ndb.StringProperty
    weiboId = ndb.StringProperty
    wechatId = ndb.StringProperty
    qqId = ndb.StringProperty
    created = ndb.DateTimeProperty(auto_now_add=True)



