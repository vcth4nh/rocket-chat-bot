from marshmallow import Schema, fields, ValidationError, post_load, validates
from bson import ObjectId
from datetime import datetime

# Helper để xử lý ObjectId
class ObjectIdField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if not isinstance(value, ObjectId):
            raise ValidationError("Invalid ObjectId")
        return str(value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return ObjectId(value)
        except Exception:
            raise ValidationError("Invalid ObjectId format")


# Schema cho User
class UserSchema(Schema):
    username = fields.Str(required=True, validate=lambda x: 3 <= len(x) <= 30)
    email = fields.Email(required=False)
    password = fields.Str(required=True)
    is_active = fields.Bool(default=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_load
    def set_defaults(self, data, **kwargs):
        """
        Thiết lập giá trị mặc định cho các trường.
        """
        data["created_at"] = data.get("created_at", datetime.utcnow())
        data["updated_at"] = data.get("updated_at", datetime.utcnow())
        return data


class PolicyRuleSchema(Schema):
    type = fields.String(
        required=True,
        validate=lambda t: t in ["regex", "blacklist", "length_limit", "detect_secrets"],
        description="Type of the rule (regex, blacklist, length_limit, detect_secrets)",
    )
    value = fields.Raw(required=True, description="Value for the policy rule (string or int)")
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @validates("value")
    def validate_value(self, value):
        if self.context.get("type") == "length_limit" and not isinstance(value, int):
            raise ValidationError("Value must be an integer for type 'length_limit'")
        if self.context.get("type") in ["regex", "blacklist"] and not isinstance(value, str):
            raise ValidationError("Value must be a string for type 'regex' or 'blacklist'")
        if self.context.get("type") == "detect_secrets" and not isinstance(value, bool):
            raise ValidationError("Value must be a boolean for type 'detect_secrets'")
        

from pydantic import BaseModel, Field, EmailStr, validator
from bson import ObjectId
from datetime import datetime
from typing import Optional

# Custom ObjectId Type for Pydantic
class PydanticObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class UserBaseModel(BaseModel):
    username: str
    email: Optional[EmailStr]
    is_active: bool = True

class UserCreateModel(BaseModel):
    username: str
    password: str
    is_active: bool = True

