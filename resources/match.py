__author__ = 'crespowang'

from flask_restful import Resource, reqparse, marshal_with, fields
import logging
from datetime import datetime
from time import strptime, mktime
import calendar
from datastore.match import Match


class UTCTime(fields.Integer):
    def format(self, value):
        logging.debug(value)
        logging.debug(calendar.timegm(datetime.now().timetuple()))
        if isinstance(value, datetime):
            logging.debug(calendar.timegm(value.utctimetuple()))
            return calendar.timegm(value.utctimetuple())
        return None


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

resource_field = {
    "id": fields.String,
    "location": fields.String,
    "startTime": UTCTime,
    "finishTime": UTCTime,
    "checkinEarliest": UTCTime,
    "checkinLatest": UTCTime,
    "created": UTCTime,
}

get_resource_fields = {
    'matches': fields.Nested(resource_field)
}


post_resource_fields = {
    'match': fields.Nested(resource_field)
}

class Matches(Resource):

    @marshal_with(get_resource_fields)
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
                "created": match.createdTime
            })


        return {'matches': matches_json}


    @marshal_with(post_resource_fields)
    def post(self):
        logging.debug("creating match")
        args = parser.parse_args()
        match_details = args
        match = Match.create(args.get('startTime'), args.get('finishTime'), args.get('checkinEarliest'),
                             args.get('checkinLatest'), args.get('location'))

        match_details['id'] = match.id()
        return {'match': match_details}

    def put(self):
        logging.debug("updating a match")
        return {'hello': 'australia'}


