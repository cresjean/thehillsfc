
import logging
from flask import Flask
from resources.match import Matches
from flask_restful import Api



app = Flask(__name__)
app.config['DEBUG'] = True
api = Api(app)

api.add_resource(Matches, '/api/matches')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

