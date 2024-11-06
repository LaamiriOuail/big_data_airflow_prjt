import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from sqlalchemy.ext.declarative import declarative_base
from config import App_Settings




# Create the base class
Base = declarative_base()

DATABASE_URL:str=App_Settings.database_url

print(DATABASE_URL)

def import_models():
    # Import all models
    from models.user import UserModel
    from models.product import ProductModel
    from models.transaction import TransactionModel

def init_db():
    # Import all models
    import_models()
    # Create an engine
    engine = create_engine(DATABASE_URL)  # Change the URL according to your database setup
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine, checkfirst=True)
    return session