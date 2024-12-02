from flask import Blueprint, jsonify, request
from ..models import db, Subscription, Player, PlayerTroop, TroopConfiguration

# 创建蓝图
personal_troops_routes = Blueprint('personal_troops_routes', __name__)


@personal_troops_routes.route('/', methods=['GET'])
def get_personal_troops(username):
    try:
        # 1. 获取用户名对应的昵称
        subscription = Subscription.query.filter_by(username=username).first()
        if not subscription or not subscription.nickname:
            return jsonify({'message': 'Nickname not found for the given username'}), 404

        nickname = subscription.nickname

        # 2. 查询玩家的 PlayerID
        player = Player.query.filter_by(Nickname=nickname).first()
        if not player:
            return jsonify({'message': 'Player not found for the given nickname'}), 404

        player_id = player.PlayerID

        # 3. 查询玩家的部队信息
        troops = (
            db.session.query(
                PlayerTroop.ConfigurationID,
                PlayerTroop.Power,
                TroopConfiguration.General1,
                TroopConfiguration.General2,
                TroopConfiguration.General3
            )
            .join(TroopConfiguration, PlayerTroop.ConfigurationID == TroopConfiguration.ConfigurationID)
            .filter(PlayerTroop.PlayerID == player_id)
            .all()
        )

        # 4. 构造返回数据
        troop_list = [
            {
                'general1': troop.General1,
                'general2': troop.General2,
                'general3': troop.General3,
                'power': troop.Power
            }
            for troop in troops
        ]

        return jsonify({'troops': troop_list}), 200
    except Exception as e:
        print(f"Error fetching personal troops: {e}")
        return jsonify({'message': 'Internal server error'}), 500
