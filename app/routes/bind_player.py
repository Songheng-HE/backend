from flask import Blueprint, request, jsonify
from .. import db
from ..models import Player, Subscription

bind_player_routes = Blueprint('bind_player_routes', __name__)

@bind_player_routes.route('/', methods=['POST', 'OPTIONS'])
def bind_player():
    if request.method == 'OPTIONS':
        # 处理预检请求，返回 204 状态码
        return '', 204

    # 处理实际的 POST 请求
    data = request.get_json()
    nickname = data.get('nickname')

    # 查找玩家
    player = Player.query.filter_by(Nickname=nickname).first()

    if player:
        current_user = Subscription.query.filter_by(username=request.headers.get('username')).first()
        if current_user:
            current_user.nickname = nickname
            db.session.commit()
            return jsonify({'message': 'Character bound successfully!'}), 200
        else:
            return jsonify({'message': 'User not found!'}), 404
    else:
        return jsonify({'message': 'Character not found!'}), 404
