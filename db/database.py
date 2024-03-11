import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Create engine
engine = create_engine(os.environ["MYSQL_DATABASE_URI"])

# Create Session class
session = scoped_session(sessionmaker(bind=engine))
