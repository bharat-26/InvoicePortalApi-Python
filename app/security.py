import bcrypt
import jwt
import random
from datetime import datetime, timedelta, timezone

from app.config import get_settings


def verify_password(password: str, password_hash: str):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8")
    )

def generate_otp():
    return str(random.randint(100000, 999999))


def create_access_token(user_id: int, email: str):
    settings = get_settings()

    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_expiry_minutes
    )

    payload = {
        "user_id": user_id,
        "email": email,
        "exp": expire_time
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm="HS256"
    )

    return token