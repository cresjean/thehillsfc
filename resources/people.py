__author__ = 'crespowang'
from flask_restful import Resource, reqparse, marshal_with, fields
import logging
from resource_fields import *
from datastore.people import People
from ext.util import UTCTime
parser = reqparse.RequestParser()

parser.add_argument("name", type=str, location='json', required=True,
                    help="Name cannot be blank")

parser.add_argument("position", type=str, location='json')
parser.add_argument("wechatId", type=str, location='json')





class PeopleResource(Resource):

    @marshal_with(people_resource_field)
    def get(self, people_id):
        people = People.getone(people_id)

        people.__setattr__('id', people_id)

        logging.debug(people)
        return {"people": people}


class PeoplesResource(Resource):

    @marshal_with(people_resource_field)
    def get(self):

        people = People.getall()
        for person in people:
            person.__setattr__('id', person.key.id())

        logging.debug(people)
        return {"people": people}

    @marshal_with(people_resource_field)
    def post(self):
        logging.debug("creating people")
        args = parser.parse_args()
        people_details = args
        people = People.create(args.get('name'), args.get('position'), args.get('wechatId'))

        people_details['id'] = people.id()

        return {'people': people_details}