from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from .database import session

Base = declarative_base()
Base.query = session.query_property()


class ShortenedURL(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True)
    original_url = Column(String(512), nullable=False)
    shortened_url = Column(String(128), nullable=False, unique=True)
