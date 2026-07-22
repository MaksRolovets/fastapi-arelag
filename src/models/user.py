from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from db.base import BaseModel


class User(BaseModel):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=True, unique=True)
    status = Column(String, nullable=True)
    created = Column(DateTime, nullable=True)

    user_balance = relationship("UserBalance", back_populates="owner")


