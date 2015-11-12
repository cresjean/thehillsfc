__author__ = 'crespowang'
from google.appengine.ext import ndb
from people import People
import string, random
import logging

class Match(ndb.Model):
    location = ndb.StringProperty(indexed=False)
    startTime = ndb.DateTimeProperty()
    finishTime = ndb.DateTimeProperty()
    signinEarliest = ndb.DateTimeProperty()
    signinLatest = ndb.DateTimeProperty()
    createdTime = ndb.DateTimeProperty(auto_now_add=True)
    signupCode = ndb.StringProperty()
    signinCode = ndb.StringProperty()
    registerdPeople = ndb.KeyProperty(kind=People, repeated=True)
    participatedPeople = ndb.KeyProperty(kind=People, repeated=True)
    status = ndb.StringProperty()

    @classmethod
    def create(cls, start, finish, signinEarliest, checkInLatest, location):
        match = Match()
        match.populate(location=location, startTime=start, finishTime=finish,
                       signinLatest=checkInLatest, signinEarliest=signinEarliest,
                       signupCode=cls.code_generator(), signinCode=cls.code_generator(), status='OPEN')
        return match.put()

    @classmethod
    def getone(cls, id):
        return Match.get_by_id(long(id))

    @classmethod
    def getall(cls):
        q = cls.query()
        return q.fetch()

    def signup(self, peopleId):
        self.registerdPeople.append(ndb.Key('People', long(peopleId)))
        self.put()

    def signin(self, peopleId):
        self.participatedPeople.append(ndb.Key('People', long(peopleId)))
        self.put()

    @classmethod
    def code_generator(cls, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
