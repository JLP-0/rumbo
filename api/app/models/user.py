import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

class User(TimestampMixin, Base):
    __tablename__= "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name : Mapped[str] = mapped_column(String(120))
    timezone:Mapped[str] = mapped_column(String(64), default="America/Costa_Rica")
 