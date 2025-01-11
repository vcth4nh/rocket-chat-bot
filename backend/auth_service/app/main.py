import sys
from pathlib import Path

# # Thêm đường dẫn tuyệt đối của thư mục gốc vào sys.path
# sys.path.append(str(Path(__file__).resolve().parent.parent))
# print(sys.path)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, user, policy

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép mọi nguồn gốc, thay "*" bằng domain cụ thể nếu cần
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
    allow_headers=["*"],  # Cho phép tất cả các headers
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(policy.router, prefix="/policy", tags=["Policy"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the ChatGPT Policy!"}