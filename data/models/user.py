import uuid
from sqlalchemy import Column, String , DateTime,Float
from sqlalchemy.orm import relationship
import os
import sys
from typing import Union
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from models import Base

import datetime


# Define the User model
class UserModel(Base):
    __tablename__ = 'users'
    __extend_existing__ = True

    user_id = Column(String(37), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    city = Column(String(255), nullable=True)
    birthdate = Column(DateTime, nullable=False)

    # Optional: If you need a relationship (like transactions linked to users)
    transactions = relationship("TransactionModel", back_populates="user")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, name={self.name}, email={self.email})>"