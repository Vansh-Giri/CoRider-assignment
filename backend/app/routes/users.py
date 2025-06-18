from flask import Blueprint, request, jsonify, session
from app.models.user import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.find_all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('name', 'email', 'password')):
            return jsonify({'error': 'Missing required fields: name, email, password'}), 400
        
        # Validate email format
        email = data['email'].lower().strip()
        if '@' not in email or '.' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Check if email already exists
        if User.email_exists(email):
            return jsonify({'error': 'Email address already exists'}), 409
        
        # Validate password length
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Validate name
        name = data['name'].strip()
        if len(name) < 2:
            return jsonify({'error': 'Name must be at least 2 characters long'}), 400
        
        user = User(
            name=name,
            email=email,
            password=data['password']
        )
        user.save()
        
        # Auto-login the user after registration
        session['user_id'] = user.id
        
        return jsonify({
            'user': user.to_dict(),
            'message': 'Account created and logged in successfully',
            'auto_login': True
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # If updating email, check for duplicates
        if 'email' in data:
            new_email = data['email'].lower().strip()
            existing_user = User.find_by_email(new_email)
            if existing_user and existing_user.id != user_id:
                return jsonify({'error': 'Email address already exists'}), 409
            data['email'] = new_email
        
        success = User.update_by_id(user_id, data)
        if success:
            updated_user = User.find_by_id(user_id)
            return jsonify(updated_user.to_dict()), 200
        else:
            return jsonify({'error': 'Failed to update user'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        success = User.delete_by_id(user_id)
        if success:
            return jsonify({'message': 'User deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete user'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
