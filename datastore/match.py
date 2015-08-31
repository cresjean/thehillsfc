__author__ = 'crespowang'
from google.appengine.ext import ndb
from people import People
import logging

class Match(ndb.Model):
    location = ndb.StringProperty(indexed=False)
    startTime = ndb.DateTimeProperty()
    finishTime = ndb.DateTimeProperty()
    checkinEarliest = ndb.DateTimeProperty()
    checkinLatest = ndb.DateTimeProperty()
    createdTime = ndb.DateTimeProperty(auto_now_add=True)
    registerdPeople = ndb.KeyProperty(kind=People, repeated=True)
    participatedPeople = ndb.KeyProperty(kind=People, repeated=True)

    @classmethod
    def create(cls, start, finish, checkinEarliest, checkInLatest, location):
        match = Match()
        match.populate(location=location, startTime=start, finishTime=finish,
                       checkinLatest=checkInLatest, checkinEarliest=checkinEarliest)
        return match.put()

    @classmethod
    def getone(cls, id):
        return Match.get_by_id(long(id))

    @classmethod
    def getall(cls):
        q = cls.query()
        return q.fetch()

    def register(self, peopleId):
        self.registerdPeople.append(ndb.Key('People', long(peopleId)))
        self.put()

