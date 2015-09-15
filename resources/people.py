__author__ = 'crespowang'


from flask_restful import reqparse, marshal_with, Resource as Flask_Resource
import logging
from login import *
from resource_fields import *
from datastore.people import People
from exceptions import UserAlreadyExistsError, InvalidLoginError
from auth import Resource
from login import User
from flask.ext.login import current_user

parser = reqparse.RequestParser()


parser.add_argument("name", type=str, location='json')
parser.add_argument("position", type=str, location='json')
parser.add_argument("wechatId", type=str, location='json')
parser.add_argument("username", type=str, location='json')
parser.add_argument("password", type=str, location='json')


class PeopleLogoutResource(Flask_Resource):

    def get(self):
        logout_user()
        return ('', 204)

class PeopleLoginResource(Flask_Resource):

    def get(self):
        if current_user.is_authenticated():
            return {"status": True}
        else:
            raise InvalidLoginError


    def post(self):
        args = parser.parse_args()
        password = args.get('password')
        username = args.get('username')
        login_status = False
        people = None
        if username and password:
            people = People.getbyusername(username)
            login_status = True if people and people.validpassword(password) else False
            if login_status:
                login_user(User.get(username), remember=True)

        if not login_status:
            raise InvalidLoginError

        return {"username": username, "name": people.name, "admin": people.admin}


class PeopleResource(Resource):

    @marshal_with(people_resource_field)
    def get(self, people_id):
        people = People.getone(people_id)
        people.__setattr__('id', people_id)
        return {"people": people}


class PeoplesResource(Flask_Resource):

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
        if People.getbyusername(args.get('username')):
            logging.warning("Username already taken")
            raise UserAlreadyExistsError
        else:

            people = People.create(args.get('name'), args.get('username'))
            people.get().genpass(args.get('password'))
            people_details['id'] = people.id()

        return {'people': people_details}

