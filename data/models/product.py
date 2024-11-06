import uuid
from sqlalchemy import Column, String , DateTime,Float
from sqlalchemy.orm import relationship
import os
import sys
from typing import Union
parent_dir = os.path.abspath(os.path.join(os.getcwd(), 'data'))
sys.path.append(parent_dir)
from models import Base

import datetime

# Define the Product model
class ProductModel(Base):
    __tablename__ = 'products'
    __extend_existing__ = True

    product_id = Column(String(37), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_name = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)

    # Optional: If you need a relationship (like transactions linked to products)
    transactions = relationship("TransactionModel", back_populates="product")

    def __repr__(self):
        return f"<Product(product_id={self.product_id}, product_name={self.product_name}, price={self.price})>"

