import uuid
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.errors import UnauthorizedError
from app.core.security import decode_acces_token
from app.models import User
from app.repositories.user_repository import UserRepository

DbSession = Annotated[Session, Depends(get_db)]
_bearer = HTTPBearer(auto_error=False)

def get_currer_user(
        db: DbSession,
        credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)]
) -> User:

    if credentials is None:
        raise UnauthorizedError("Missing bearer token")
    subject = decode_acces_token(credentials.credentials)
    try: 
        user_id = uuid.UUID(subject)
    except ValueError as exc:
        raise UnauthorizedError("Invalid token subjet") from exc
    user = UserRepository(db).get_by_id(user_id)
    if user is None:
        raise UnauthorizedError("User not found")
    return user

CurrentUser = Annotated[User, Depends(get_currer_user)]
