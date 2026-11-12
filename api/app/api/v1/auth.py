from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.deps import DbSession
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest,db:DbSession):
    return AuthService(db).register(data)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: DbSession):
    return TokenResponse(access_token=AuthService(db).login(data))
