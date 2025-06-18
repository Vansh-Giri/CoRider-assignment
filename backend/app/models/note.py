import uuid
from datetime import datetime
from app.utils.database import db_instance

class Note:
    def __init__(self, title, content, user_id, note_id=None, created_at=None, updated_at=None):
        self.id = note_id or str(uuid.uuid4())
        self.title = title
        self.content = content
        self.user_id = user_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }

    def save(self):
        db = db_instance.get_db()
        note_data = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        result = db.notes.insert_one(note_data)
        return result.inserted_id

    @staticmethod
    def find_by_user_id(user_id):
        db = db_instance.get_db()
        notes = list(db.notes.find({'user_id': user_id}))
        return [Note._from_dict(note) for note in notes]

    @staticmethod
    def find_by_id(note_id, user_id):
        db = db_instance.get_db()
        note_data = db.notes.find_one({'id': note_id, 'user_id': user_id})
        return Note._from_dict(note_data) if note_data else None

    @staticmethod
    def update_by_id(note_id, user_id, update_data):
        db = db_instance.get_db()
        update_data['updated_at'] = datetime.utcnow()
        result = db.notes.update_one(
            {'id': note_id, 'user_id': user_id},
            {'$set': update_data}
        )
        return result.modified_count > 0

    @staticmethod
    def delete_by_id(note_id, user_id):
        db = db_instance.get_db()
        result = db.notes.delete_one({'id': note_id, 'user_id': user_id})
        return result.deleted_count > 0

    @staticmethod
    def _from_dict(data):
        if not data:
            return None
        return Note(
            title=data['title'],
            content=data['content'],
            user_id=data['user_id'],
            note_id=data['id'],
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
