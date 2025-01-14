from pymongo.collection import Collection
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from bson import ObjectId
from pydantic import BaseModel
from app.utils import verify_password_sha256
from fastapi.security import OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta
from app.models import Token, TokenData
from app.config import SECRET_KEY, ALGORITHM

# @app.get("/protected")
# async def protected_route(token: str = Depends()):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     return {"message": "Welcome to protected route!"}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthController:
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def authenticate_user(username: str, password: str, users_collection: Collection):
        user = users_collection.find_one({"username": username})
        if not user or not verify_password_sha256(password, user["password"]):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        access_token = AuthController.create_access_token(data={"sub": username})
        return {"access_token": access_token, "token_type": "bearer"}
        # return {"user_id": str(user["_id"]), "username": user["username"]}
