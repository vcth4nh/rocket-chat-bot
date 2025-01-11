from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from app.models import PolicyRuleSchema


class PolicyController:
    schema = PolicyRuleSchema()

    @staticmethod
    def create_policy_rule(data: dict, policy_collection: Collection):
        """
        Tạo một policy rule mới.
        """
        schema = PolicyRuleSchema()
        validated_data = schema.load(data)
        validated_data["created_at"] = datetime.utcnow()
        validated_data["updated_at"] = datetime.utcnow()
        result = policy_collection.insert_one(validated_data)
        validated_data["_id"] = result.inserted_id
        return schema.dump(validated_data)

    @staticmethod
    def get_policy_rule_by_id(policy_id: str, policy_collection: Collection):
        """
        Lấy thông tin policy rule theo ID.
        """
        policy = policy_collection.find_one({"_id": ObjectId(policy_id)})
        if not policy:
            raise HTTPException(status_code=404, detail="Policy rule not found")
        return PolicyRuleSchema().dump(policy)

    @staticmethod
    def get_all_policy_rules(policy_collection: Collection):
        """
        Lấy danh sách tất cả policy rules.
        """
        policies = list(policy_collection.find())
        return PolicyRuleSchema(many=True).dump(policies)

    @staticmethod
    def update_policy_rule(policy_id: str, update_data: dict, policy_collection: Collection):
        """
        Cập nhật thông tin policy rule.
        """
        schema = PolicyRuleSchema(partial=True)
        validated_data = schema.load(update_data)
        validated_data["updated_at"] = datetime.utcnow()
        result = policy_collection.update_one(
            {"_id": ObjectId(policy_id)}, {"$set": validated_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Policy rule not found")
        updated_policy = policy_collection.find_one({"_id": ObjectId(policy_id)})
        return schema.dump(updated_policy)

    @staticmethod
    def delete_policy_rule(policy_id: str, policy_collection: Collection):
        """
        Xóa một policy rule theo ID.
        """
        result = policy_collection.delete_one({"_id": ObjectId(policy_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Policy rule not found")
        return {"message": "Policy rule deleted successfully"}
