__author__ = 'crespowang'
from flask_restful import Resource, abort
from functools import wraps
from flask.ext.login import current_user
import logging

def basic_authentication():
    try:
        return current_user.is_authenticated
    except TypeError as e:
        logging.warn("not auth {}".format(e))
        return False

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        acct = basic_authentication()

        if acct:
            return func(*args, **kwargs)

        abort(401)
    return wrapper


class Resource(Resource):
    method_decorators = [authenticate]