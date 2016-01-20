__author__ = 'crespowang'
from flask_restful import fields

from datetime import datetime
import calendar

class UTCTime(fields.Integer):
    def format(self, value):
        if isinstance(value, datetime):

            return calendar.timegm(value.utctimetuple())
        return None
