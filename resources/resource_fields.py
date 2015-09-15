__author__ = 'crespowang'
from flask_restful import fields
from ext.util import UTCTime

# People Resource
people_field = {
    "id": fields.String,
    "name": fields.String,
    "position": fields.String,
    "weiboId": fields.String,
    "qqId": fields.String,
    "wechatId": fields.String,
    "facebookId": fields.String,
    "createdTime": UTCTime
}

people_resource_field = {
    "people": fields.Nested(people_field)
}


login_resource_field = {
    "username": fields.String,
    "password": fields.String
}


# Match Resource
match_field = {
    "id": fields.String,
    "location": fields.String,
    "startTime": UTCTime,
    "finishTime": UTCTime,
    "checkinEarliest": UTCTime,
    "checkinLatest": UTCTime,
    "createdTime": UTCTime,
    "checkinLink": fields.String,
    "regLink": fields.String
}

match_resource_fields = {
    'match': fields.Nested(match_field)
}

matches_resource_fields = {
    'matches': fields.Nested(match_field)
}


play_field = {
    "id": fields.String,
    "match_detail": fields.Nested(match_field),
    "people_detail": fields.Nested(people_resource_field),
    "registeredTime": UTCTime,
    "checkinTime": UTCTime
}

play_of_match_resource_field = play_field
play_of_match_resource_field.__delitem__('match_detail')

plays_resource_field = {

    "plays": fields.Nested(play_field)
}


play_resource_field = {
    "play": fields.Nested(play_field)
}


plays_of_match_resource_field = {
    "plays": fields.Nested(play_of_match_resource_field)
}