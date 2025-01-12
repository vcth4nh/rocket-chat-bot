from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from typing import List, Dict, Any, Optional


class Repository:
    def __init__(self, db_uri: str, db_name: str, collection_name: str):
        try:
            self.client = MongoClient(db_uri)
            self.database = self.client[db_name]
            self.collection: Collection = self.database[collection_name]
            print("Connecting to MongoDB...")
            self.test_connection()
            print(f"Connected to MongoDB collection: {db_name}.{collection_name}")
        except PyMongoError as e:
            print(f"Error connecting to MongoDB:\n{e}")
            raise
    
    def test_connection(self):
        return self.client.server_info()

    def insert_one(self, document: Dict[str, Any]) -> str:
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def insert_many(self, documents: List[Dict[str, Any]]) -> List[str]:
        result = self.collection.insert_many(documents)
        return [str(id) for id in result.inserted_ids]

    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.collection.find_one(query)

    def find_many(self, query: Dict[str, Any], limit: int = 0) -> List[Dict[str, Any]]:
        cursor = self.collection.find(query).limit(limit)
        return list(cursor)

    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        result = self.collection.update_one(query, {"$set": update})
        return result.modified_count

    def delete_one(self, query: Dict[str, Any]) -> int:
        result = self.collection.delete_one(query)
        return result.deleted_count

    def delete_many(self, query: Dict[str, Any]) -> int:
        result = self.collection.delete_many(query)
        return result.deleted_count

    def count_documents(self, query: Dict[str, Any]) -> int:
        return self.collection.count_documents(query)
    
class PolicyRepository(Repository):
    def __init__(self, db_uri: str):
        super().__init__(db_uri, db_name="chatbot_db", collection_name="policy_rules")

    def get_length_limit(self) -> Dict[str, Any]:
        query = {"type": "length_limit"}
        res = self.find_one(query)
        return int(res.get("value")) if res else None
    
    def get_detect_secrets(self) -> Dict[str, Any]:
        query = {"type": "detect_secrets"}
        res = self.find_one(query)
        return bool(res.get("value")) if res else None
    
    def get_blacklist_words(self) -> List[str]:
        query = {"type": "blacklist"}
        res = self.find_many(query)
        blacklist_words = [item.get("value") for item in res]
        return blacklist_words
    
    def get_regex_patterns(self) -> List[str]:
        query = {"type": "regex"}
        res = self.find_many(query)
        regex_patterns = [item.get("value") for item in res]
        return regex_patterns

    def find_by_policy_type(self, policy_type: str) -> Dict[str, Any]:
        query = {"type": policy_type}
        print(self.find_one(query))
        return self.find_many(query)

