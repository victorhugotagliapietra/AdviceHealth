from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from flask_jwt_extended import create_access_token
import datetime
import logging

bp = Blueprint('auth_routes', __name__, url_prefix='/auth')

logging.basicConfig(level=logging.DEBUG)

@bp.route('/register', methods=['POST'])
def register():
  try:
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
      return jsonify({'error': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
      return jsonify({'error': 'Username already exists'}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201
  except Exception as e:
    logging.error(f"Error occurred: {e}")
    return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
  try:
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
      return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
      return jsonify({'error': 'Invalid username or password'}), 401

    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=str(user.id), expires_delta=expires)

    return jsonify({'access_token': access_token}), 200
  except Exception as e:
    logging.error(f"Error occurred: {e}")
    return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500
