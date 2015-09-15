__author__ = 'crespowang'

from flask_restful import reqparse, marshal_with, fields
import logging
from datetime import datetime
from time import strptime, mktime
from datastore.match import Match
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

parser.add_argument("checkinLatest", type=datetime_parser, location='json', required=True,
                    help="Latest check-in time cannot be blank")

parser.add_argument("checkinEarliest", type=datetime_parser, location='json', required=True,
                    help="Earliest check-in time cannot be blank")

parser.add_argument("location", type=str, location='json', required=True,
                    help="Location cannot be blank")



class MatchPlayers(Resource):


    @marshal_with(people_resource_field)
    def get(self, match_id):
        match = Match.getone(match_id)
        if match is None:
            raise MatchNotExistsError
        registered_people = []

        for ple in match.registerdPeople:
            registered_people.append(ple.get())

        logging.debug(registered_people)
        return {"people": registered_people}


class MatchResource(Resource):

    @marshal_with(match_resource_fields)
    def get(self, match_id):
        match = Match.getone(match_id)
        plays = Play.getbyMatch(match_id)
        match.__setattr__('id', match_id)

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
                "checkinEarliest": match.checkinEarliest,
                "checkinLatest": match.checkinLatest,
                "createdTime": match.createdTime
            })


        return {'matches': matches_json}


    @marshal_with(match_resource_fields)
    def post(self):
        logging.debug("creating match")
        args = parser.parse_args()
        match_details = args
        match = Match.create(args.get('startTime'), args.get('finishTime'), args.get('checkinEarliest'),
                             args.get('checkinLatest'), args.get('location'))

        match_details['id'] = match.id()
        match_details['checkinLink'] = "{}/checkin/{}/{}".format(host_url, match.id(), match.get().checkinCode)
        match_details['regLink'] = "{}/reg/{}/{}".format(host_url, match.id(), match.get().regCode)
        return {'match': match_details}

    def put(self):
        logging.debug("updating a match")
        return {'hello': 'australia'}


class MatchHelper():
    @classmethod
    def verfy_checkin(cls, match_id, code):
        match = Match.getone(match_id)
        if code == match.checkinCode:
            logging.debug("Checkin user {}".format(current_user.key_id))
            # match.register(current_user)
            return True
        return False
