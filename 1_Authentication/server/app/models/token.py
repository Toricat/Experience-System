from sqlalchemy import Boolean, Column, Integer, String
from .base import Base

class Token(Base):
    id = Column(Integer, primary_key=True, index=True)
    access_token=Column(String(225), index=True)
    refresh_token=Column(String(225), index=True)
