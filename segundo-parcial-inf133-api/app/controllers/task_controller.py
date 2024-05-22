from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.task_model import Task
from app.models.user_model import User
from app.utils.decorators import role_required

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    status = data.get('status', 'Pending')
    created_at = data.get('created_at')
    assigned_to = data.get('assigned_to')

    user = User.query.filter_by(email=assigned_to).first()
    if not user:
        return jsonify({"msg": "Assigned user not found"}), 404

    new_task = Task(title=title, description=description, status=status, created_at=created_at, assigned_to=user.email)
    new_task.save()
    return jsonify({"msg": "Task created successfully"}), 201

@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    tasks = Task.get_all()
    return jsonify([task.to_dict() for task in tasks]), 200

@task_bp.route('/tasks/<int:id>', methods=['GET'])
@jwt_required()
def get_task(id):
    task = Task.get_by_id(id)
    if not task:
        return jsonify({"msg": "Task not found"}), 404
    return jsonify(task.to_dict()), 200

@task_bp.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    task = Task.get_by_id(id)
    if not task:
        return jsonify({"msg": "Task not found"}), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.assigned_to = data.get('assigned_to', task.assigned_to)
    task.update()
    return jsonify({"msg": "Task updated successfully"}), 200

@task_bp.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    task = Task.get_by_id(id)
    if not task:
        return jsonify({"msg": "Task not found"}), 404
    task.delete()
    return jsonify({"msg": "Task deleted successfully"}), 204

