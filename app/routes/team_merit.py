from flask import Blueprint, jsonify
from ..models import db, Player, Team
from sqlalchemy.sql import func

team_merit_routes = Blueprint('team_merit_routes', __name__)

@team_merit_routes.route('/', methods=['GET'])
def team_merit_rank():
    # Query to calculate the sum of merits for each team in guildID 101
    results = db.session.query(
        Team.TeamName,
        func.sum(Player.Merit).label('total_merit')
    ).join(Team, Player.TeamID == Team.TeamID
    ).filter(Team.GuildID == 101
    ).group_by(Team.TeamName
    ).order_by(func.sum(Player.Merit).desc()
    ).all()

    # Prepare the response
    rank_list = [
        {
            'TeamID': index + 1,  # 添加 TeamID
            'TeamName': result.TeamName,
            'Merit': result.total_merit  # 修改字段名为 Merit
        }
        for index, result in enumerate(results)
    ]
    return jsonify({'teams': rank_list})

