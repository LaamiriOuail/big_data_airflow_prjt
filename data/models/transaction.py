import uuid
from sqlalchemy import Column, String , DateTime,Float,ForeignKey
from sqlalchemy.orm import relationship
import os
import sys
from typing import Union
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from models import Base

import datetime


# Define the Transaction model
class TransactionModel(Base):
    __tablename__ = 'transactions'
    __extend_existing__ = True

    transaction_id = Column(String(37), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(37), ForeignKey('users.user_id'), nullable=False)
    product_id = Column(String(37), ForeignKey('products.product_id'), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Define relationships
    user = relationship("UserModel", back_populates="transactions")
    product = relationship("ProductModel", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction(transaction_id={self.transaction_id}, user_id={self.user_id}, product_id={self.product_id}, amount={self.amount})>"
