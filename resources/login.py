__author__ = 'crespowang'

from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user
import logging
from datastore.people import People

login_manager = LoginManager()

class UserNotFoundError(Exception):
    logging.warning("User not found")
    pass


class User(UserMixin):
    def __init__(self, username):
        logging.debug("Login {}".format(username))
        people = People.getbyusername(username)
        if not people:
            raise UserNotFoundError()
        self.username = username
        self.name = people.name
        self.id = people.username
        self.key_id = people.key.id()
        self.password = people.password

    @classmethod
    def get(self_class, username):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(username)
        except UserNotFoundError:
            return None


@login_manager.user_loader
def load_user(username):
    return User.get(username)


