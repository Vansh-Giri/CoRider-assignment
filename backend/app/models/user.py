import uuid
from datetime import datetime
import bcrypt
from app.utils.database import db_instance

class User:
    def __init__(self, name, email, password, user_id=None, created_at=None):
        self.id = user_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = self._hash_password(password) if password else None
        self.created_at = created_at or datetime.utcnow()

    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Check if provided password matches the hashed password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }

    def save(self):
        db = db_instance.get_db()
        user_data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at
        }
        result = db.users.insert_one(user_data)
        return result.inserted_id

    @staticmethod
    def find_all():
        db = db_instance.get_db()
        users = list(db.users.find({}, {'password': 0}))
        return [User._from_dict(user) for user in users]

    @staticmethod
    def find_by_id(user_id):
        db = db_instance.get_db()
        user_data = db.users.find_one({'id': user_id}, {'password': 0})
        return User._from_dict(user_data) if user_data else None

    @staticmethod
    def find_by_email(email):
        """Find user by email address"""
        db = db_instance.get_db()
        user_data = db.users.find_one({'email': email}, {'password': 0})
        return User._from_dict(user_data) if user_data else None

    @staticmethod
    def email_exists(email):
        """Check if email already exists in database"""
        db = db_instance.get_db()
        user = db.users.find_one({'email': email})
        return user is not None

    @staticmethod
    def authenticate(email, password):
        """Authenticate user with email and password"""
        db = db_instance.get_db()
        user_data = db.users.find_one({'email': email})
        if user_data:
            user = User._from_dict_with_password(user_data)
            if user and user.check_password(password):
                return user
        return None

    @staticmethod
    def update_by_id(user_id, update_data):
        db = db_instance.get_db()
        if 'password' in update_data:
            update_data['password'] = bcrypt.hashpw(
                update_data['password'].encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
        
        result = db.users.update_one(
            {'id': user_id}, 
            {'$set': update_data}
        )
        return result.modified_count > 0

    @staticmethod
    def delete_by_id(user_id):
        db = db_instance.get_db()
        # Also delete user's notes
        db.notes.delete_many({'user_id': user_id})
        result = db.users.delete_one({'id': user_id})
        return result.deleted_count > 0

    @staticmethod
    def _from_dict(data):
        if not data:
            return None
        return User(
            name=data['name'],
            email=data['email'],
            password=None,  # Don't expose password
            user_id=data['id'],
            created_at=data['created_at']
        )

    @staticmethod
    def _from_dict_with_password(data):
        """Create user object with password (for authentication)"""
        if not data:
            return None
        user = User(
            name=data['name'],
            email=data['email'],
            password=None,  # Don't set password directly
            user_id=data['id'],
            created_at=data['created_at']
        )
        user.password = data['password']  # Set hashed password for verification
        return user
