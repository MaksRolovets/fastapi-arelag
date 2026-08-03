from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from db.base import BaseModel

class UserBalance(BaseModel):
    __tablename__ = "user_balance"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    currency = Column(String, nullable=True)
    amount = Column(Numeric, nullable=True)
    created = Column(DateTime, nullable=True)
    UniqueConstraint('user_id', 'currency', name='user_balance_user_currency_unique')

    owner = relationship("User", back_populates="user_balance")