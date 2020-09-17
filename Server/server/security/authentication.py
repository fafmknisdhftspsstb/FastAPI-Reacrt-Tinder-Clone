from datetime import datetime, timedelta
from typing import Optional
from server import pwd_context
from pydantic import BaseModel

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
