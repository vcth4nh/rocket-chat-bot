from fastapi import APIRouter, Depends
from app.database import db
from app.controllers.auth_controller import AuthController

router = APIRouter()

@router.post("/login")
def login(username: str, password: str):
    """
    API route để đăng nhập người dùng.
    """
    users_collection = db["users"]  # Tham chiếu tới collection `users` trong MongoDB
    result = AuthController.authenticate_user(username, password, users_collection)
    return {"message": "Login successful", "data": result}
