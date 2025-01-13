from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException
from app.models import PolicyCreateModel, PolicyUpdateModel


class PolicyController:

    @staticmethod
    def create_policy_rule(data: PolicyCreateModel, policy_collection: Collection):
        
        validated_data_dict = data.model_dump()
        validated_data_dict["created_at"] = validated_data_dict.get("created_at") or datetime.utcnow()
        validated_data_dict["updated_at"] = validated_data_dict.get("updated_at") or datetime.utcnow()

        if validated_data_dict.get("type") in ["length_limit", "detect_secrets"]:
            inserted_id = policy_collection.update_one(
                {"type": validated_data_dict.get("type")},
                {"$set": validated_data_dict},
                upsert=True
            ).upserted_id
        else:
            inserted_id = policy_collection.insert_one(validated_data_dict).inserted_id
        return {"id": str(inserted_id)}
    
    @staticmethod
    def get_policy_rule_by_type(policy_type: str, policy_collection: Collection):
        policy = policy_collection.find({"type": policy_type})
        if not policy:
            raise HTTPException(status_code=404, detail="Policy rule not found")
        res = []
        for p in policy:
            p["_id"] = str(p["_id"])
            res.append(p)
        return res

    @staticmethod
    def get_all_policy_rules(policy_collection: Collection):
        policies = list(policy_collection.find())
        res = []
        for po in policies:
            po["_id"] = str(po["_id"])
            res.append(po)
        return res

    @staticmethod
    def update_policy_rule(policy_id: str, data: PolicyUpdateModel, policy_collection: Collection):
        """
        Cập nhật thông tin policy rule.
        """
        validated_data_dict = data.model_dump()
        validated_data_dict["updated_at"] = validated_data_dict.get("updated_at") or datetime.utcnow()

        result = policy_collection.update_one(
            {"_id": ObjectId(policy_id)}, {"$set": validated_data_dict}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Policy rule not found")
        updated_policy = policy_collection.find_one({"_id": ObjectId(policy_id)})
        updated_policy["_id"] = str(updated_policy["_id"])
        return updated_policy

    @staticmethod
    def delete_policy_rule(policy_id: str, policy_collection: Collection):
        """
        Xóa một policy rule theo ID.
        """
        result = policy_collection.delete_one({"_id": ObjectId(policy_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Policy rule not found")
        return {"message": "Policy rule deleted successfully"}
