from datetime import datetime
from pymongo.collection import Collection
from bson import ObjectId
from fastapi import HTTPException
from app.schemas import UserSchema
from app.models import UserCreateModel, UserGetModel
import hashlib
from app.utils import hash_password_sha256


class UserController:

    @staticmethod
    def create_user(data: UserCreateModel, users_collection: Collection):

        if users_collection.find_one({"email": data.username}):
            raise HTTPException(status_code=400, detail="Email already registered")
        if users_collection.find_one({"username": data.username}):
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = hash_password_sha256(data.password)
        validated_data_dict = data.model_dump()
        validated_data_dict["password"] = hashed_password
        validated_data_dict["created_at"] = validated_data_dict.get("created_at") or datetime.utcnow()
        validated_data_dict["updated_at"] = validated_data_dict.get("updated_at") or datetime.utcnow()

        inserted_id = users_collection.insert_one(validated_data_dict).inserted_id
        return {"id": str(inserted_id)}

    @staticmethod
    def get_user_by_id(user_id: str, users_collection: Collection):
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user["_id"] = str(user["_id"])
        return user

    @staticmethod
    def update_user(user_id: str, data: dict, users_collection: Collection):
        try:
            validated_data = UserCreateModel.model_validate(data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")

        updated_data = validated_data.model_dump(exclude_unset=True)
        updated_data["updated_at"] = datetime.utcnow()

        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": updated_data}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User updated successfully"}

    @staticmethod
    def delete_user(user_id: str, users_collection: Collection):
        result = users_collection.delete_one({"_id": ObjectId(user_id)})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User deleted successfully"}
    
    @staticmethod
    def get_all_users(users_collection: Collection):
        users = users_collection.find()
        res = []
        for user in users:
            user["_id"] = str(user["_id"])
            res.append(user)
        return res
