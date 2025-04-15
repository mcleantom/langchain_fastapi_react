from datetime import datetime, UTC

from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    sub = Column(String(255), unique=True, nullable=False, primary_key=True)

    sessions = relationship("Session", back_populates="user")


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(255), ForeignKey('users.sub'), nullable=False)
    name = Column(String(255))
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)

    user = relationship("User", back_populates="sessions")
