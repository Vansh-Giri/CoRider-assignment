from pymongo import MongoClient
from app.config import Config

class Database:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def connect(self):
        if self._client is None:
            self._client = MongoClient(Config.MONGODB_URI)
            self._db = self._client.get_default_database()
        return self._db

    def get_db(self):
        if self._db is None:
            self.connect()
        return self._db

db_instance = Database()
