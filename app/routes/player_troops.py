from flask import Blueprint, jsonify, request
from ..models import db, Player, PlayerTroop, TroopConfiguration

# 创建蓝图
player_troops_routes = Blueprint('player_troops_routes', __name__)

@player_troops_routes.route('/', methods=['GET'])
def get_player_troops(nickname):
    try:
        # 查找玩家是否存在
        player = Player.query.filter_by(Nickname=nickname).first()
        if not player:
            return jsonify({'message': 'Player not found'}), 404

        # 查找玩家的部队信息
        troops = (
            db.session.query(
                PlayerTroop.ConfigurationID,
                PlayerTroop.Power,
                TroopConfiguration.General1,
                TroopConfiguration.General2,
                TroopConfiguration.General3
            )
            .join(TroopConfiguration, PlayerTroop.ConfigurationID == TroopConfiguration.ConfigurationID)
            .filter(PlayerTroop.PlayerID == player.PlayerID)
            .all()
        )

        # 构造返回数据
        troop_list = [
            {
                'general1': troop.General1,
                'general2': troop.General2,
                'general3': troop.General3,
                'power': troop.Power,
            }
            for troop in troops
        ]

        return jsonify({'troops': troop_list}), 200

    except Exception as e:
        print(f"Error fetching player troops: {e}")
        return jsonify({'message': 'Internal server error'}), 500
