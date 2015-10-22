__author__ = 'crespowang'
from flask_restful import HTTPException

class UserAlreadyExistsError(HTTPException):
    pass

class MatchNotExistsError(HTTPException):
    pass

class InvalidLoginError(HTTPException):
    pass

class PlayNotExistsError(HTTPException):
    pass