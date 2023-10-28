from datetime import datetime, timezone

from flask import request, jsonify, Blueprint, current_app
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, current_user, get_jwt

from app import db, redis_conn
from app.schemas import user_schema
from app.models import User
from app.auth.handlers import *

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    user_data = request.json
    try:
        user = user_schema.load(user_data)
        user.set_password(user_data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'})
    except ValidationError as err:
        return jsonify(err.messages), 400
    except IntegrityError:
        db.session.rollback()  # Rollback en caso de error
        return jsonify({'message': 'Username or email already registered'}), 400

@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # Get user in database
    user = User.query.filter_by(username=username).first()

    # Verify user and password
    if user and user.check_password(password):
        access_token = create_access_token(identity=user)
        return jsonify({'access_token': access_token})

    return jsonify({'message': 'Invalid username or password'}), 401

@bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    token_expires = get_jwt()['exp']
    now = datetime.now(timezone.utc)
    remaining_time = token_expires - int(now.timestamp())

    redis_conn.set(jti, '', ex=remaining_time)

    return jsonify(msg='Access token revoked')

@bp.route('/verify', methods=['GET'])
@jwt_required()
def verify():
    return jsonify(message=f'Verify endpoint for {current_user.username}')