from fastapi import APIRouter
from app.database.database import db
from app.controllers.policy_controller import PolicyController
from app.models import PolicyCreateModel, PolicyUpdateModel

router = APIRouter()

@router.post("/policies")
def create_policy_rule(policy: PolicyCreateModel):
    """
    Tạo một policy rule mới.
    """
    policy_collection = db["policy_rules"]
    result = PolicyController.create_policy_rule(policy, policy_collection)
    return {"message": "Policy rule created successfully", "data": result}

@router.get("/policies")
def get_all_policy_rules():
    """
    Lấy danh sách tất cả policy rules.
    """
    policy_collection = db["policy_rules"]
    result = PolicyController.get_all_policy_rules(policy_collection)
    return {"data": result}

@router.get("/policies/{policy_id}")
def get_policy_rule(policy_id: str):
    """
    Lấy thông tin policy rule theo ID.
    """
    policy_collection = db["policy_rules"]
    result = PolicyController.get_policy_rule_by_id(policy_id, policy_collection)
    return {"data": result}


@router.put("/policies/{policy_id}")
def update_policy_rule(policy_id: str, update_data: PolicyUpdateModel):
    """
    Cập nhật thông tin policy rule.
    """
    policy_collection = db["policy_rules"]
    result = PolicyController.update_policy_rule(policy_id, update_data, policy_collection)
    return {"message": "Policy rule updated successfully", "data": result}


@router.delete("/policies/{policy_id}")
def delete_policy_rule(policy_id: str):
    """
    Xóa một policy rule theo ID.
    """
    policy_collection = db["policy_rules"]
    result = PolicyController.delete_policy_rule(policy_id, policy_collection)
    return result

@router.get("/policies_by_type/{policy_type}")
def get_policy_rule_by_type(policy_type: str):
    """
    Lấy danh sách policy rules theo type.
    """
    policy_collection = db["policy_rules"]
    result = PolicyController.get_policy_rule_by_type(policy_type, policy_collection)
    return {"data": result}