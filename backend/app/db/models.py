from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    suid = Column(String(255), unique=True, nullable=False)

    sessions = relationship("Session", back_populates="user")


class Session(Base):
    __tablename__ = 'sessions'

    id: str = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: int = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    name: str = Column(String(255))

    user = relationship("User", back_populates="sessions")
