from flask import Blueprint
from .register import register_routes
from .bind_player import bind_player_routes
from .login import login_routes
from .team_merit import team_merit_routes  # Import the team merit routes
from .personal_troops import personal_troops_routes
from .player_troops import player_troops_routes


main = Blueprint('main', __name__)

# 注册子路由
main.register_blueprint(register_routes, url_prefix='/register')
main.register_blueprint(bind_player_routes, url_prefix='/bind')
main.register_blueprint(login_routes, url_prefix='/auth')
main.register_blueprint(team_merit_routes, url_prefix='/team-merit-rank')  # Register the blueprint
main.register_blueprint(personal_troops_routes, url_prefix='/api/personal-troops/<string:username>')
main.register_blueprint(player_troops_routes, url_prefix='/api/player-troops/<string:nickname>')
