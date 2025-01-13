from pymongo.collection import Collection
from passlib.context import CryptContext
from fastapi import HTTPException
from bson import ObjectId
from pydantic import BaseModel
from app.utils import verify_password_sha256


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthController:
    @staticmethod
    def authenticate_user(username: str, password: str, users_collection: Collection):
        user = users_collection.find_one({"username": username})
        if not user or not verify_password_sha256(password, user["password"]):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        return {"user_id": str(user["_id"]), "username": user["username"]}
