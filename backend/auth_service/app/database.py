from app.config import DATABASE_NAME, MONGO_URI
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from typing import Any
import logging

class MongoDB:
    def __init__(self, uri: str, database_name: str):
        self._uri = uri
        self._database_name = database_name
        self._client: Any = None
        self._database: Any = None

    def connect(self):
        try:
            self._client = MongoClient(self._uri)
            self._database = self._client[self._database_name]
            logging.info(f"Successfully connected to MongoDB: {self._database_name}")
        except ConnectionFailure as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            raise e

    def get_database(self):
        if self._database is None:
            raise ConnectionFailure("Database connection has not been established.")
        return self._database

    def close(self):
        if self._client:
            self._client.close()
            logging.info("MongoDB connection closed.")


mongo_instance = MongoDB(MONGO_URI, DATABASE_NAME)
mongo_instance.connect()
db = mongo_instance.get_database()
