from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(225), index=False)
    email = Column(String(225), unique=True, index=True, nullable=False)
    hashed_password = Column(String(225), nullable=False)
    image = Column(String(225), nullable=True)
    role = Column(String(225), nullable=False, default="user")
    account_type = Column(String(225), nullable=False, default="local")
    is_active = Column(Boolean,nullable=False, default=False)
    verify =  relationship("Verify", back_populates="owner",uselist=False )
    token = relationship("Token", back_populates="owner",uselist=False )
    item = relationship("Item", back_populates="user", uselist=False)
