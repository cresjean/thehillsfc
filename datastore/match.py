__author__ = 'crespowang'
from google.appengine.ext import ndb


class Match(ndb.Model):
    location = ndb.StringProperty(indexed=False)
    startTime = ndb.DateTimeProperty()
    finishTime = ndb.DateTimeProperty()
    checkinEarliest = ndb.DateTimeProperty()
    checkinLatest = ndb.DateTimeProperty()
    createdTime = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    @ndb.transactional
    def create(cls, start, finish, checkinEarliest, checkInLatest, location):
        match = Match()
        match.populate(location=location, startTime=start, finishTime=finish,
                       checkinLatest=checkInLatest, checkinEarliest=checkinEarliest)
        return match.put()

    @classmethod
    def getall(cls):
        q = cls.query()
        return q.fetch()
