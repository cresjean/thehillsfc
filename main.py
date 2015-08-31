import logging
from flask import Flask
from resources.match import MatchesResource, MatchResource, MatchPlayers
from resources.people import PeopleResource, PeoplesResource
from resources.play import PlayResource, PlayMatchResource
from flask_restful import Api

app = Flask(__name__)
app.config['DEBUG'] = True
api = Api(app)

api.add_resource(MatchesResource, '/api/matches')
api.add_resource(MatchResource, '/api/matches/<match_id>')
api.add_resource(PeoplesResource, '/api/people')
api.add_resource(PeopleResource, '/api/people/<people_id>')
api.add_resource(PlayResource, '/api/play')
api.add_resource(MatchPlayers, '/api/matches/<match_id>/registered-people')
api.add_resource(PlayMatchResource, '/api/matches/<match_id>/plays')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

