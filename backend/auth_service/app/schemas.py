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
    id = ObjectIdField(data_key="_id", dump_only=True)
    username = fields.Str(required=True, validate=lambda x: 3 <= len(x) <= 30)
    email = fields.Email(required=True)
    hashed_password = fields.Str(required=True)
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
        validate=lambda t: t in ["regex", "blacklist", "length_limit"],
        description="Type of the rule (regex, blacklist, length_limit)"
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
