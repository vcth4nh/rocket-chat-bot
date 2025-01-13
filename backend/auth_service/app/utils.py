from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from bson import ObjectId
import hashlib
import os
import base64

def hash_password_sha256(password: str, salt: Optional[str] = None) -> str:
    """Hash a password using SHA256 with an optional salt."""
    if not salt:
        salt = base64.b64encode(os.urandom(16)).decode('utf-8')  # Generate a random salt
    password_bytes = f"{salt}{password}".encode("utf-8")
    hashed_password = hashlib.sha256(password_bytes).hexdigest()
    return f"{salt}${hashed_password}"


def verify_password_sha256(password: str, hashed_password: str) -> bool:
    """Verify a password against a SHA256 hash with salt."""
    try:
        salt, stored_hash = hashed_password.split("$")
    except ValueError:
        raise ValueError("Invalid hashed password format")
    return hash_password_sha256(password, salt) == hashed_password