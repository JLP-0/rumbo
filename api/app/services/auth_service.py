from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import ConflictError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, db: Session) ->None:
        self.db = db
        self.users = UserRepository(db)

    def register(self, data: RegisterRequest)-> User:
        email = data.email.lower()
        if self.users.get_by_email(email):
            raise ConflictError("Email already registered")

        user = User(
            email= email,
            password_hash= hash_password(data.password),
            full_name = data.full_name
        )

        try:
            self.users.add(user)
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError("Email already registered") from exc

        self.db.refresh(user)
        return user

    def login(self, data: LoginRequest)-> str:
        user = self.users.get_by_email(data.email.lower())
        if user is None or not verify_password(data.password, user.password_hash):
            raise UnauthorizedError("Invalid Email or password")
        return create_access_token(str(user.id))