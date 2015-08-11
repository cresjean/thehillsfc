from flask import Flask
from match import Match
from flask import json
import logging
from flask.views import MethodView
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.



@app.route('/app')
def dev():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'



class MatchAPI(MethodView):

    def get(self, match_id):
        if match_id is None:
            logging.debug("Match ID is none, listing matches")
        else:
            logging.debug("Match ID {}".format(match_id))



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

