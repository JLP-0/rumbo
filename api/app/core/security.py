from datetime import UTC, datetime, timedelta

import jwt 
from pwdlib import PasswordHash

from app.core.config import get_settings
from app.core.errors import UnauthorizedError

_password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return _password_hash.hash(password)

def verify_password(password:str, hashed:str) -> bool:
    return _password_hash.verify(password, hashed)

def create_access_token(subject:str)-> str:
    settings = get_settings()
    now = datetime.now(UTC)
    payload = {
        "sub": subject,
        "iat": now,
        "exp": now + timedelta(minutes=settings.access_token_expire_minutes)
    }

    return jwt.encode(payload, settings.jwt_secret_key, algorithm= settings.jwt_algorithm)

def decode_acces_token(token:str)-> str:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except jwt.InvalidTokenError as exc:
        raise UnauthorizedError("Invalid or expired token") from exc
    subject = payload.get("sub")
    if not subject:
        raise UnauthorizedError("Invalid token payload")
    return subject