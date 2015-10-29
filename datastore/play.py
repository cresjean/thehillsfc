__author__ = 'crespowang'
from google.appengine.ext import ndb
from datastore.people import People
from datastore.match import Match


class Play(ndb.Model):
    people = ndb.KeyProperty(kind=People)
    match = ndb.KeyProperty(kind=Match)
    team = ndb.StringProperty()
    leave = ndb.BooleanProperty(default=False)
    signupMissing = ndb.BooleanProperty(default=False)
    score = ndb.FloatProperty(default=6)
    signupTime = ndb.DateTimeProperty(auto_now_add=True)
    signinTime = ndb.DateTimeProperty()

    @classmethod
    def create(cls, peopleId, matchId, leave=False, missing=False):
        play = Play()
        play.populate(people=ndb.Key('People', long(peopleId)), match=ndb.Key('Match', long(matchId)), leave=leave, signupMissing = missing)
        return play.put()


    @classmethod
    def getone(cls, id):
        return Play.get_by_id(long(id))


    @classmethod
    def getall(cls):
        q = cls.query()
        return q.fetch()

    @classmethod
    def getbyMatchPeople(cls, matchId, peopleId):
        return cls.query(cls.match == ndb.Key('Match', long(matchId)),
                         cls.people == ndb.Key("People", long(peopleId))).get()

    @classmethod
    def getbyMatch(cls, matchId):
        return cls.query(cls.match == ndb.Key('Match', long(matchId))).fetch()

