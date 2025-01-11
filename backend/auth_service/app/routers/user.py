from fastapi import APIRouter
from app.database import db
from app.controllers.user_controller import UserController

router = APIRouter()

@router.post("/users")
def create_user(user: dict):
    users_collection = db["users"]
    result = UserController.create_user(user, users_collection)
    return {"message": "User created successfully", "data": result}



@router.get("/users")
def get_all_users():
    users_collection = db["users"]
    result = UserController.get_all_users(users_collection)
    return {"data": result}

@router.get("/users/search")
def search_user(username: str):
    users_collection = db["users"]
    result = UserController.search_user_by_username(username, users_collection)
    return {"data": result}

@router.patch("/users/{user_id}/deactivate")
def deactivate_user(user_id: str):
    users_collection = db["users"]
    result = UserController.deactivate_user(user_id, users_collection)
    return result

@router.patch("/users/{user_id}/activate")
def activate_user(user_id: str):
    users_collection = db["users"]
    result = UserController.activate_user(user_id, users_collection)
    return result

@router.get("/users/{user_id}")
def get_user_by_id(user_id: str):
    users_collection = db["users"]
    result = UserController.get_user_by_id(user_id, users_collection)
    return {"data": result}

@router.put("/users/{user_id}")
def update_user(user_id: str, update_data: dict):
    users_collection = db["users"]
    result = UserController.update_user(user_id, update_data, users_collection)
    return {"message": "User updated successfully", "data": result}

@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    users_collection = db["users"]
    result = UserController.delete_user(user_id, users_collection)
    return result
