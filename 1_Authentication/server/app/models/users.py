from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(225), index=True)
    email = Column(String(225), unique=True, index=True, nullable=False)
    hashed_password = Column(String(225), nullable=False)
    is_active = Column(Boolean, default=True)
    image = Column(String(225), nullable=True)
    items = relationship("Item", back_populates="owner", lazy="selectin")
    tokens = relationship("Token", back_populates="owner", lazy="selectin")
