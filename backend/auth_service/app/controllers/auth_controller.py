from pymongo.collection import Collection
from passlib.context import CryptContext
from fastapi import HTTPException
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthController:
    @staticmethod
    def authenticate_user(username: str, password: str, users_collection: Collection):
        """
        Xác thực thông tin người dùng trong MongoDB.
        """
        user = users_collection.find_one({"username": username})
        if not user or not pwd_context.verify(password, user["hashed_password"]):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return {"user_id": str(user["_id"]), "username": user["username"]}
