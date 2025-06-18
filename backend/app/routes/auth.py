from flask import Blueprint, request, jsonify, session
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({'error': 'Missing email or password'}), 400
        
        user = User.authenticate(data['email'], data['password'])
        if user:
            # Store user session
            session['user_id'] = user.id
            return jsonify({
                'message': 'Login successful',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/current-user', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.find_by_id(user_id)
        if user:
            return jsonify(user.to_dict()), 200
    return jsonify({'error': 'Not authenticated'}), 401

@auth_bp.route('/verify-password', methods=['POST'])
def verify_password():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        
        if not user_id or not password:
            return jsonify({'error': 'Missing user_id or password'}), 400
        
        # Get user with password for verification
        from app.utils.database import db_instance
        db = db_instance.get_db()
        user_data = db.users.find_one({'id': user_id})
        
        if user_data:
            user = User._from_dict_with_password(user_data)
            if user and user.check_password(password):
                return jsonify({'valid': True}), 200
        
        return jsonify({'valid': False}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login-with-password', methods=['POST'])
def login_with_password():
    """Login user by ID and password verification"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        
        if not user_id or not password:
            return jsonify({'error': 'Missing user_id or password'}), 400
        
        # Get user with password for verification
        from app.utils.database import db_instance
        db = db_instance.get_db()
        user_data = db.users.find_one({'id': user_id})
        
        if user_data:
            user = User._from_dict_with_password(user_data)
            if user and user.check_password(password):
                # Log the user in
                session['user_id'] = user.id
                return jsonify({
                    'message': 'Login successful',
                    'user': user.to_dict()
                }), 200
        
        return jsonify({'error': 'Invalid password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
