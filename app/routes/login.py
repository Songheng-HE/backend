from flask import Blueprint, request, jsonify
from ..models import Subscription

login_routes = Blueprint('login_routes', __name__)

@login_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # 获取用户名和密码
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required.'}), 400

    # 查找用户
    user = Subscription.query.filter_by(username=username).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found.'}), 404

    # 验证密码
    if user.password != password:
        return jsonify({'success': False, 'message': 'Incorrect password.'}), 401

    # 登录成功
    return jsonify({'success': True, 'message': 'Login successful!'}), 200
