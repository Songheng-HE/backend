from flask import Blueprint, request, jsonify
from .. import db
from ..models import Subscription

register_routes = Blueprint('register_routes', __name__)

@register_routes.route('/', methods=['POST'])
def register():
    data = request.get_json()
    # 默认nickname为空
    new_user = Subscription(
        username=data['username'],
        password=data['password'],
        membership_duration=data['membership'],
        nickname=None  # 初始化为None或空字符串
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully!'}), 201
