import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists 

database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/chreddit')
engine = create_engine(database_url)
Session = sessionmaker()
Session.configure(bind=engine)

Base = declarative_base()
class Submission(Base):
    __tablename__ = 'submission'
    id = Column(Integer, primary_key=True)
    title = Column(String)

Base.metadata.create_all(engine)

def submit(title):
    submission = Submission(title=title)
    session = Session()
    session.add(submission)
    session.commit()

def exists(title):
    session = Session()
    result = session.query(exists().where(Submission.title==title)).scalar()
    return result 


 
