from datetime import datetime
from typing import Optional
from pydantic import BaseModel, validator, EmailStr, root_validator
from bson import ObjectId
from pydantic.fields import Field

class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, field=None, config=None):
        if not ObjectId.is_valid(value):
            raise ValueError(f"Invalid ObjectId: {value}")
        return ObjectId(value)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, field_schema):
        field_schema.update(type="string")
        return field_schema

    def __str__(self):
        return str(super().__str__())

class UserBaseModel(BaseModel):
    username: str
    password: str

    @validator("username")
    def validate_username(cls, value):
        if not (3 <= len(value) <= 30):
            raise ValueError("Username must be between 3 and 30 characters long")
        if not value.isalnum():
            raise ValueError("Username must be alphanumeric")
        return value

    @validator("password")
    def validate_password(cls, value):
        # if len(value) < 8:
        #     raise ValueError("Password must be at least 8 characters long")
        # if not any(char.isdigit() for char in value):
        #     raise ValueError("Password must contain at least one digit")
        # if not any(char.isupper() for char in value):
        #     raise ValueError("Password must contain at least one uppercase letter")
        # if not any(char.islower() for char in value):
        #     raise ValueError("Password must contain at least one lowercase letter")
        # if not any(char in "!@#$%^&*()_+" for char in value):
        #     raise ValueError("Password must contain at least one special character (!@#$%^&*()_+)")
        return value
    
class LoginModel(UserBaseModel):
    pass

class UserCreateModel(UserBaseModel):
    is_active: bool = True
    email: str | None = None

class UserGetModel(UserBaseModel):
    id: PydanticObjectId | None = Field(default=None, alias="_id")
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        json_encoders = {ObjectId: lambda obj: str(obj)}
        arbitrary_types_allowed = True

class PolicyBaseModel(BaseModel):
    type: str
    value: str | int | bool

    @validator("type")
    def validate_type(cls, value):
        if value not in ["regex", "blacklist", "length_limit", "detect_secrets"]:
            raise ValueError("Invalid policy type")
        return value
    
    @root_validator(pre=True)
    def validate_policy(cls, values):
        policy_type = values.get("type")
        policy_value = values.get("value")

        if policy_type not in ["regex", "blacklist", "length_limit", "detect_secrets"]:
            raise ValueError("Invalid policy type")

        if policy_type == "length_limit" and not isinstance(policy_value, int):
            raise ValueError("Value must be an integer for type 'length_limit'")

        if policy_type in ["regex", "blacklist"] and not isinstance(policy_value, str):
            raise ValueError("Value must be a string for type 'regex' or 'blacklist'")

        if policy_type == "detect_secrets" and not isinstance(policy_value, bool):
            raise ValueError("Value must be a boolean for type 'detect_secrets'")

        return values

class PolicyCreateModel(PolicyBaseModel):
    pass

class PolicyUpdateModel(PolicyBaseModel):
    pass

class PolicyGetModel(PolicyBaseModel):
    id: PydanticObjectId | None = Field(default=None, alias="_id")
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        json_encoders = {ObjectId: lambda obj: str(obj)}
        arbitrary_types_allowed = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None