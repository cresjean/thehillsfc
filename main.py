import logging
from flask import Flask
from flask import redirect
from resources.match import MatchesResource, MatchResource, MatchPlayers, MatchHelper
from resources.people import PeopleResource, PeoplesResource, PeopleLoginResource, PeopleLogoutResource
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
    'InvalidLoginError': {
        'message': "The login details are not right",
        'status': 401
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
api.add_resource(PeopleLogoutResource, '/api/people/logout')


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@login_required
@app.route('/checkin/<matchid>/<code>')
def match_checkin(matchid, code):
    logging.debug("Checkin match {} code {}".format(matchid, code))
    checkin_status = MatchHelper.checkin(matchid, code)
    if checkin_status:
        logging.debug("YEEAP")
        return redirect('/#/checkin/{}'.format(matchid))
    else:
        logging.debug("NOPPP")
    return redirect('/')


@login_required
@app.route('/reg/<matchid>/<code>')
def match_registration(matchid, code):
    logging.debug("register match {} code {}".format(matchid, code))
    checkin_status = MatchHelper.register(matchid, code)
    if checkin_status:
        logging.debug("YEEAP")
        return redirect('/#/checkin/{}'.format(matchid))
    else:
        logging.debug("NOPPP")
    return redirect('/')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


