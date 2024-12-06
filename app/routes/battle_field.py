from flask import Blueprint, request, jsonify
from ..models import db, Guild, Team, Player, Battle
from sqlalchemy.sql import func, case
from datetime import datetime, timedelta

battle_field_routes = Blueprint('battle_field_routes', __name__)

# 获取所有工会
@battle_field_routes.route('/api/guilds/', methods=['GET'])
def get_guilds():
    guilds = Guild.query.all()
    guild_list = [{'GuildID': guild.GuildID, 'GuildName': guild.GuildName} for guild in guilds]
    return jsonify({'guilds': guild_list}), 200

# 根据工会获取团队
@battle_field_routes.route('/api/teams/<int:guild_id>', methods=['GET'])
def get_teams(guild_id):
    # 通过路径参数 guild_id 获取对应的团队信息
    teams = Team.query.filter_by(GuildID=guild_id).all()
    team_list = [{'TeamID': team.TeamID, 'TeamName': team.TeamName, 'GuildID': team.GuildID} for team in teams]
    return jsonify({'teams': team_list}), 200


# 获取战场考勤数据
@battle_field_routes.route('/api/battle-attendance', methods=['POST'])
def get_battle_field_data():
    data = request.get_json()
    print(f"Received data: {data}")  # 打印接收到的数据

    teams = data.get('teams', [])
    team_ids = [team['TeamID'] for team in teams if 'TeamID' in team]
    time_range = data.get('time_range', 'past24h')
    print(f"Team IDs: {team_ids}, Time Range: {time_range}")  # 打印解析后的数据


    # 时间范围计算
    now = datetime.utcnow()
    if time_range == 'past12h':
        start_time = now - timedelta(hours=12)
    elif time_range == 'past24h':
        start_time = now - timedelta(hours=24)
    elif time_range == 'past week':
        start_time = now - timedelta(days=7)
    else:
        return jsonify({'message': 'Invalid time range'}), 400

    # 查询战场数据
    query = (
        db.session.query(
            Player.Nickname,
            func.count(Battle.BattleID).label('battle_count'),
            func.sum(case((Battle.LandOcc == True, 1), else_=0)).label('lands_occupied'),
            func.sum(case((Battle.BuildingsDestroyed == True, 1), else_=0)).label('buildings_destroyed'),
            func.avg(Battle.CasualtyRatio).label('average_casualty_ratio'),
            func.sum(case((Battle.Result == 'Win', 1), else_=0)).label('wins')
        )
        .join(Battle, Player.PlayerID == Battle.AttackerPlayerID)
        .filter(Battle.DateTime >= start_time)
        .group_by(Player.Nickname)
    )

    if team_ids:
        query = query.filter(Player.TeamID.in_(team_ids))

    query = query.group_by(Player.PlayerID).order_by(func.count(Battle.BattleID).desc())

    results = query.all()

    # 打印结果到后端控制台
    for result in results:
        print(f"Nickname: {result.Nickname}, Battle Count: {result.battle_count}, "
              f"Lands Occupied: {result.lands_occupied}, "
              f"Buildings Destroyed: {result.buildings_destroyed}, "
              f"Average Casualty Ratio: {result.average_casualty_ratio:.2f}, "
              f"Wins: {result.wins}")


    # 返回数据
    attendance_data = [
        {
            'nickname': result.Nickname,
            'battle_count': result.battle_count,
            'lands_occupied': result.lands_occupied  or 0,
            'buildings_destroyed': result.buildings_destroyed  or 0,
            'average_casualty_ratio': round(result.average_casualty_ratio, 2) if result.average_casualty_ratio  else None,
            'win_rate': round(result.wins / result.battle_count * 100, 2) if result.battle_count  else 0
        }
        for result in results
    ]

    return jsonify({'attendance': attendance_data}), 200

