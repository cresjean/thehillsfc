import logging
from flask import Flask
from flask import redirect
from resources.match import MatchesResource, MatchResource, MatchPlayers
from resources.people import PeopleResource, PeoplesResource, PeopleLoginResource
from resources.play import PlayResource, PlayMatchResource
from flask_restful import Api
from flask.ext.login import login_required, logout_user

from resources.login import login_manager
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "asdbiu324yuihuebwfksdf9bkj234!@#$@"

login_manager.init_app(app)

custom_errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'MatchNotExistsError': {
        'message': "The match ID does not exist",
        'status': 404,
    }
}

api = Api(app, errors=custom_errors)
api.add_resource(MatchesResource, '/api/matches')
api.add_resource(MatchResource, '/api/matches/<match_id>')
api.add_resource(PeoplesResource, '/api/people')
api.add_resource(PeopleResource, '/api/people/<people_id>')
api.add_resource(PlayResource, '/api/play')
api.add_resource(MatchPlayers, '/api/matches/<match_id>/registered-people')
api.add_resource(PlayMatchResource, '/api/matches/<match_id>/plays')
api.add_resource(PeopleLoginResource, '/api/people/login')


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


