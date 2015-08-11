__author__ = 'crespowang'
from google.appengine.ext import ndb


class Match(ndb.Model):
    location = ndb.StringProperty(indexed=False)
    startTime = ndb.DateTimeProperty()
    endTime = ndb.DateTimeProperty()
    checkinEarliest = ndb.DateTimeProperty()
    checkinLatest = ndb.DateTimeProperty()
    createdTime = ndb.DateTimeProperty(auto_now_add=True)

