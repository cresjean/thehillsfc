__author__ = 'crespowang'

from flask_restful import reqparse, marshal_with, fields
import logging
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
                "signupTime": play.signupTime,
                "signinTime": play.signinTime,
                "signinOntime": True if play.signinTime and play.signinTime < match.signinLatest else False,
                "signinLate": True if play.signinTime and play.signinTime > match.signinLatest else False
            })

        return {"people": registered_people}


class MatchResource(Resource):

    @marshal_with(match_resource_fields)
    def get(self, match_id):
        match = Match.getone(match_id)
        match.__setattr__('id', match_id)

        match.__setattr__('signinLink', "http://{}/match-signin/{}/{}".format(host_url, match_id, match.signinCode))
        match.__setattr__('signupLink', "http://{}/match-signup/{}/{}".format(host_url, match_id, match.signupCode))
        match.__setattr__('signupCode', match.signupCode)

        return {"match": match}


class MatchesResource(Resource):

    @marshal_with(matches_resource_fields)
    def get(self):
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
                "createdTime": match.createdTime
            })
        return {'matches': matches_json}


    @marshal_with(match_resource_fields)
    def post(self):
        logging.debug("creating match")
        args = parser.parse_args()
        match_details = args
        match = Match.create(args.get('startTime'), args.get('finishTime'), args.get('signinEarliest'),
                             args.get('signinLatest'), args.get('location'))

        match_details['id'] = match.id()

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
            return {"status": False, "reason": "You are too late for sign in", "code": 1}

        people = People.getone(current_user.key_id)
        if people and people.key in match.participatedPeople:
            logging.debug("You have already signed in")
            return {"status": False, "reason": "You have already signed in", "code": 0}

        if match and code == match.signinCode:
            logging.debug("Sign in user {}".format(current_user.key_id))
            match.signin(current_user.key_id)
            play = Play.getbyMatchPeople(match_id, current_user.key_id)
            play.signinTime = datetime.now()
            play.put()


            return {"status": True}
        return {"status": False}

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
            return True
        return False