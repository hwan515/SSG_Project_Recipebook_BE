from flask import Blueprint, request, jsonify
from app import db, bcrypt, jwt_redis
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from datetime import datetime, timedelta, timezone
from flask_wtf.csrf import generate_csrf

bp = Blueprint('members', __name__, url_prefix='/members')

@bp.route('/test')
def test():
    return "test V1"

# 회원가입
@bp.route('/forms', methods=['POST'])
def signup():
    user_data = request.get_json()

    username = user_data['username']
    hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
    email = user_data['email']

    # 중복 가입 조회
    if User.query.filter_by(username=username).one_or_none():
        return jsonify({
            "result": "failed",
            "message": "중복 가입"
        }), 400

    new_user = User(username=username, password=hashed_password, email=email)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "result": "success",
        "user_id": new_user.id,
        "message": "회원가입 성공"
    }), 200

# 로그인
@bp.route('/login', methods=['POST'])
def login():
    user_data = request.get_json()
    username = user_data['username']
    password = user_data['password']

    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify({
            "result": "failed",
            "message": "등록되지 않은 아이디거나 비밀번호가 일치하지 않음"
        }), 401

    # JWT 토큰 생성 및 반환
    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
    refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(days=30))

    response = jsonify({
        "result": "success",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "message": "로그인 성공"
    })
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, 200
