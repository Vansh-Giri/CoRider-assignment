from flask import Blueprint, request, jsonify
from app.models.note import Note
from app.models.user import User

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/users/<user_id>/notes', methods=['GET'])
def get_user_notes(user_id):
    try:
        # Check if user exists
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        notes = Note.find_by_user_id(user_id)
        return jsonify([note.to_dict() for note in notes]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notes_bp.route('/users/<user_id>/notes', methods=['POST'])
def create_note(user_id):
    try:
        # Check if user exists
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if not data or not all(k in data for k in ('title', 'content')):
            return jsonify({'error': 'Missing required fields: title, content'}), 400
        
        note = Note(
            title=data['title'],
            content=data['content'],
            user_id=user_id
        )
        note.save()
        
        return jsonify(note.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notes_bp.route('/users/<user_id>/notes/<note_id>', methods=['PUT'])
def update_note(user_id, note_id):
    try:
        # Check if user exists
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        note = Note.find_by_id(note_id, user_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        success = Note.update_by_id(note_id, user_id, data)
        if success:
            updated_note = Note.find_by_id(note_id, user_id)
            return jsonify(updated_note.to_dict()), 200
        else:
            return jsonify({'error': 'Failed to update note'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notes_bp.route('/users/<user_id>/notes/<note_id>', methods=['DELETE'])
def delete_note(user_id, note_id):
    try:
        # Check if user exists
        user = User.find_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        note = Note.find_by_id(note_id, user_id)
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        success = Note.delete_by_id(note_id, user_id)
        if success:
            return jsonify({'message': 'Note deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete note'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
