from fastapi import APIRouter, Depends
from app.database.database import db
from app.controllers.auth_controller import AuthController
from app.models import LoginModel

router = APIRouter()

@router.post("/login")
def login(user: LoginModel):
    username = user.username
    password = user.password
    users_collection = db["users"]  # Tham chiếu tới collection `users` trong MongoDB
    result = AuthController.authenticate_user(username, password, users_collection)
    return {"message": "Login successful", "data": result}
