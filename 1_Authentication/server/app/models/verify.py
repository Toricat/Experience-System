from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Verify(Base):
    id = Column(Integer, primary_key=True, index=True)
    code_active=Column(String(225), index=True)
    exp_active = Column(DateTime, nullable=False)
    code_recovery=Column(String(225), index=True)
    exp_recovery=Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id" ,ondelete="CASCADE"))
    owner = relationship("User", back_populates="verify", passive_deletes=True) 