from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
import config

Base = declarative_base()

class Submission(Base):
    __tablename__ = config.tablename

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    url = Column(String)
    feed = Column(String)
    created = Column(DateTime)
    submitted = Column(DateTime)

    def __eq__(self, other):
        return isistance(other, Submission) and other.title == self.title
