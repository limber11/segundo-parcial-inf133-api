from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user_model import User
from app import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'member')

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    new_user = User(name=name, email=email, password=password, role=role)
    new_user.save()
    return jsonify({"msg": "User created successfully"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"msg": "Invalid credentials"}), 401

@user_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_users():
    users = User.get_all()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_user(id):
    user = User.get_by_id(id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@user_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_user(id):
    user = User.get_by_id(id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    user.update()
    return jsonify({"msg": "User updated successfully"}), 200

@user_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(id):
    user = User.get_by_id(id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    user.delete()
    return jsonify({"msg": "User deleted successfully"}), 204
