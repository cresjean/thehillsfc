__author__ = 'crespowang'

from flask_restful import reqparse, marshal_with, fields
import logging
from google.appengine.api import memcache
from datetime import datetime
from time import strptime, mktime
from datastore.match import Match
from datastore.people import People
from resource_fields import *
from exceptions import MatchNotExistsError
from datastore.play import Play
from auth import Resource
from appengine_config import host_url
from flask.ext.login import current_user

def datetime_parser(datetime_str):
    if datetime_str is not None:
        try:
            dt = strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.000Z")
        except Exception as e:
            logging.error(e)
            raise ValueError('{} is not a valid datetime'.format(datetime_str))
        else:
            return datetime.fromtimestamp(mktime(dt))
    else:
        raise ValueError('{} is not a valid datetime'.format(datetime_str))


parser = reqparse.RequestParser()

parser.add_argument("startTime", type=datetime_parser, location='json', required=True,
                    help="Game start time cannot be blank")

parser.add_argument("finishTime", type=datetime_parser, location='json', required=True,
                    help="Game finish time cannot be blank")

parser.add_argument("signinLatest", type=datetime_parser, location='json', required=True,
                    help="Latest check-in time cannot be blank")

parser.add_argument("signinEarliest", type=datetime_parser, location='json', required=True,
                    help="Earliest check-in time cannot be blank")

parser.add_argument("location", type=str, location='json', required=True,
                    help="Location cannot be blank")

signup_parser = reqparse.RequestParser()

signup_parser.add_argument("code", type=str, location='json', required=True,
                    help="Code cannot be blank")

leave_parser = reqparse.RequestParser()

leave_parser.add_argument("status", type=bool, location='json', required=True,
                    help="Leave status must be set")


class MatchLeave(Resource):

   def post(self, match_id):
       logging.debug("ask for leave")
       args = leave_parser.parse_args()

       status = args.get('status')
       MatchHelper.askforleave(match_id, status)
       return {"leave_status": status}


class MatchStatus(Resource):

    def post(self, match_id, status):
        statusm = {"open": "OPEN", "close": "CLOSED", "cancel": "CANCELLED"}
        if status in ['open', 'close', 'cancel']:
            logging.debug("Setting {}".format(status))
            MatchHelper.status(match_id, statusm.get(status))
        return {"status": "ok"}


class MatchSignUp(Resource):

    @marshal_with(match_resource_fields)
    def post(self, match_id):
        logging.debug("SignMeUP")
        args = signup_parser.parse_args()
        code = args.get('code')
        status = MatchHelper.signup(match_id, code)
        if status:
            match = Match.getone(match_id)
            match.__setattr__('id', match_id)
            return {"match": match}
        return {"match": None}


class MatchPlayerIn(Resource):

    def get(self, match_id, people_id):
        match = Match.getone(match_id)
        if match is None:
            raise MatchNotExistsError
        people = People.getone(people_id)
        if people.key in match.registerdPeople:
            return {"in": True}
        else:
            return {"in": False}


class MatchPlayers(Resource):

    @marshal_with(match_people_resource)
    def get(self, match_id):
        registered_people = memcache.get(match_id, "match_players")
        if not registered_people:

            match = Match.getone(match_id)
            if match is None:
                raise MatchNotExistsError
            registered_people = []
            for ple in match.registerdPeople:
                player = ple.get()
                play = Play.getbyMatchPeople(match_id, player.key.id())

                registered_people.append({
                    "name": player.name,
                    "id": player.key.id(),
                    "playId": play.key.id(),
                    "signupTime": play.signupTime,
                    "signinTime": play.signinTime,
                    "admin": player.admin,
                    "team": play.team or None,
                    "leave": play.leave,
                    "signupMissing": play.signupMissing,
                    "signinOntime": True if play.signinTime and play.signinTime < match.signinLatest else False,
                    "signinLate": True if play.signinTime and play.signinTime > match.signinLatest else False
                })
            memcache.set(match_id, registered_people, namespace="match_players")
        else:
            logging.debug("get match players from memcache")

        return {"people": registered_people}


class MatchResource(Resource):

    @marshal_with(match_resource_fields)
    def get(self, match_id):
        match_dict = memcache.get(match_id, "match")
        if not match_dict:
            match = Match.getone(match_id)
            match_dict = match.to_dict()
            match_dict['id'] = match_id
            match_dict['signinLink'] = "http://{}/match-signin/{}/{}".format(host_url, match_id, match.signinCode)
            match_dict['signupLink'] = "http://{}/match-signup/{}/{}".format(host_url, match_id, match.signupCode)
            match_dict['signupCode'] = match.signupCode

            memcache.set(match_id, match_dict, namespace="match")
        else:
            logging.debug("get match info from memcache {}")

        return {"match": match_dict}


class MatchesResource(Resource):

    @marshal_with(matches_resource_fields)
    def get(self):
        matches_json = memcache.get("matches")
        if not matches_json:
            matches = Match.getall()
            matches_json = []
            for match in matches:
                matches_json.append({
                    "id": match.key.id(),
                    "location": match.location,
                    "startTime": match.startTime,
                    "finishTime": match.finishTime,
                    "signinEarliest": match.signinEarliest,
                    "signinLatest": match.signinLatest,
                    "createdTime": match.createdTime,
                    "nosignups": len(match.registerdPeople),
                    "status": match.status
                })
            memcache.set("matches", matches_json)
        else:
            logging.debug("get matches from memcache")
        return {'matches': matches_json}


    @marshal_with(match_resource_fields)
    def post(self):
        logging.debug("creating match")
        args = parser.parse_args()
        match_details = args
        match = Match.create(args.get('startTime'), args.get('finishTime'), args.get('signinEarliest'),
                             args.get('signinLatest'), args.get('location'))

        match_details['id'] = match.id()

        memcache.flush_all()
        return {'match': match_details}

    def put(self):
        logging.debug("updating a match")
        return {'hello': 'australia'}


class MatchHelper():

    @classmethod
    def signin(cls, match_id, code):
        match = Match.getone(match_id)

        if datetime.now() < match.signinEarliest:
            logging.debug("You are too early for sign in")
            return {"status": False, "reason": "You are too early for sign in", "code": -1}
        if datetime.now() > match.signinLatest:
            logging.debug("You are too late for sign in")
            logging.debug("Sign in user {}".format(current_user.key_id))
            match.signin(current_user.key_id)

            play = Play.getbyMatchPeople(match_id, current_user.key_id)

            if play is None:
                logging.debug("this guy didn't sign up, but is sign-in now")
                match.signup(current_user.key_id)
                Play.create(current_user.key_id, match_id, missing=True)
            else:
                play.signinTime = datetime.now()
                play.put()
            memcache.flush_all()

            return {"status": False, "reason": "You are too late for sign in", "code": 1}

        people = People.getone(current_user.key_id)
        if people and people.key in match.participatedPeople:
            logging.debug("You have already signed in")
            return {"status": False, "reason": "You have already signed in", "code": 0}

        if match and code == match.signinCode:
            logging.debug("Sign in user {}".format(current_user.key_id))
            match.signin(current_user.key_id)
            play = Play.getbyMatchPeople(match_id, current_user.key_id)

            if play is None:
                logging.debug("this guy didn't sign up, but is sign-in now")
                match.signup(current_user.key_id)
                Play.create(current_user.key_id, match_id, missing=True)
            else:
                play.signinTime = datetime.now()
                play.put()

            memcache.flush_all()

            return {"status": True}
        return {"status": False}


    @classmethod
    def askforleave(cls, match_id, status):
        match = Match.getone(match_id)
        people = People.getone(current_user.key_id)
        if people and people.key in match.registerdPeople:
            logging.debug("You have already signed up! Now switch leave")
            play = Play.getbyMatchPeople(match_id, current_user.key_id)
            if play:
                play.leave = status
                play.put()
        elif people and people.key:
            match.signup(current_user.key_id)
            Play.create(current_user.key_id, match_id, leave=status)
        memcache.flush_all()

        return True

    @classmethod
    def signup(cls, match_id, code):
        match = Match.getone(match_id)

        people = People.getone(current_user.key_id)
        if people and people.key in match.registerdPeople:
            logging.debug("You have already signed up")
            return True

        if match and code == match.signupCode:
            logging.debug("Sign up user {}".format(current_user.key_id))
            match.signup(current_user.key_id)
            Play.create(current_user.key_id, match_id)
            memcache.flush_all()
            return True
        return False

    @classmethod
    def status(cls, match_id, status):
        match = Match.getone(match_id)
        logging.debug("Set status to {}".format(status))
        if match:
            match.status = status
            match.put()
            memcache.flush_all()
        return True