import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, DateTime
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
    created = Column(DateTime)

Base.metadata.create_all(engine)

def submit(title):
    submission = Submission(title=title)
    session = Session()
    session.add(submission)
    session.commit()

    #free database in heroku is limited to 10k rows, so delete old ones
    session = Session()
    result = session.query(Submission).order_by(desc(Submission.created)).offset(9500).delete()
    session.commit()

def submitted(title):
    session = Session()
    result = session.query(exists().where(Submission.title==title)).scalar()
    return result 


 
