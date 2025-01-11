from datetime import datetime
from pymongo.collection import Collection
from bson import ObjectId
from fastapi import HTTPException


class UserController:
    @staticmethod
    def create_user(data: dict, users_collection: Collection):
        """
        Tạo người dùng mới.
        :param data: Dictionary chứa thông tin người dùng.
        :param users_collection: MongoDB collection cho users.
        :return: Người dùng được tạo.
        """
        # Kiểm tra email đã tồn tại
        if users_collection.find_one({"email": data["email"]}):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        if users_collection.find_one({"username": data["username"]}):
            raise HTTPException(status_code=400, detail="Username already registered")

        # Thêm thời gian tạo và cập nhật
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()

        # Thêm người dùng vào cơ sở dữ liệu
        result = users_collection.insert_one(data)
        data["_id"] = result.inserted_id
        return data

    @staticmethod
    def get_user_by_id(user_id: str, users_collection: Collection):
        """
        Lấy thông tin người dùng theo ID.
        :param user_id: ID của người dùng.
        :param users_collection: MongoDB collection cho users.
        :return: Thông tin người dùng hoặc None nếu không tìm thấy.
        """
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def get_all_users(users_collection: Collection):
        """
        Lấy danh sách tất cả người dùng.
        :param users_collection: MongoDB collection cho users.
        :return: Danh sách người dùng.
        """
        users = list(users_collection.find())
        return users

    @staticmethod
    def update_user(user_id: str, update_data: dict, users_collection: Collection):
        """
        Cập nhật thông tin người dùng.
        :param user_id: ID của người dùng.
        :param update_data: Dictionary chứa dữ liệu cần cập nhật.
        :param users_collection: MongoDB collection cho users.
        :return: Người dùng sau khi được cập nhật.
        """
        update_data["updated_at"] = datetime.utcnow()
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return users_collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def delete_user(user_id: str, users_collection: Collection):
        """
        Xóa người dùng theo ID.
        :param user_id: ID của người dùng.
        :param users_collection: MongoDB collection cho users.
        :return: Trạng thái xóa.
        """
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    
    @staticmethod
    def search_user_by_username(username: str, users_collection: Collection):
        """
        Tìm người dùng theo username (không phân biệt chữ hoa/thường).
        """
        users = list(users_collection.find({"username": {"$regex": username, "$options": "i"}}))
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        return users

    @staticmethod
    def deactivate_user(user_id: str, users_collection: Collection):
        """
        Vô hiệu hóa tài khoản người dùng.
        """
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deactivated successfully"}

    @staticmethod
    def activate_user(user_id: str, users_collection: Collection):
        """
        Kích hoạt lại tài khoản người dùng.
        """
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": True, "updated_at": datetime.utcnow()}}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User activated successfully"}
