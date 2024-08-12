from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from models.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user") 
    image = Column(String, nullable=True)
    items = relationship("Item", back_populates="owner", lazy="selectin")
