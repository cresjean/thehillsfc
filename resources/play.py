__author__ = 'crespowang'
from flask_restful import reqparse, marshal_with, fields
import logging
from auth import Resource
from resource_fields import *
from exceptions import PlayNotExistsError
from datastore.match import Match
from datastore.play import Play
from google.appengine.api import memcache
parser = reqparse.RequestParser()

parser.add_argument("peopleId", type=int, location='json', required=True, help="People ID cannot be blank")
parser.add_argument("matchId", type=int, location='json', required=True, help="Match ID cannot be blank")

teamup_parser = reqparse.RequestParser()
teamup_parser.add_argument("team", type=str, location='json', required=True, help="Team cannot be blank")

class PlayMatchResource(Resource):

    @marshal_with(plays_of_match_resource_field)
    def get(self, match_id):
        plays = Play.getbyMatch(match_id)
        for play in plays:
            play.__setattr__('people_detail', play.people.get())
            play.__setattr__('id', play.key.id())

        return {"plays": plays}



class PlayTeamResource(Resource):

    def post(self, play_id):
        play = Play.getone(play_id)
        if not play:
            raise PlayNotExistsError
        args = teamup_parser.parse_args()
        team = args.get('team')
        play.team = team
        play.put()
        memcache.flush_all()
        return {"status": True}

class PlayResource(Resource):

    @marshal_with(plays_resource_field)
    def get(self):
        plays = Play.getall()
        for play in plays:
            play.__setattr__('match_detail', play.match.get())
            play.__setattr__('people_detail', play.people.get())
            play.__setattr__('id', play.key.id())

        return {"plays": plays}

    @marshal_with(play_resource_field)
    def post(self):
        logging.debug("creating play")
        args = parser.parse_args()
        play = Play.create(args.get('peopleId'), args.get('matchId'))
        play_details = args
        play_details['id'] = play.id()

        match = Match.getone(args.get('matchId'))
        match.register(args.get('peopleId'))

        logging.debug(match)

        return {'play': play_details}



