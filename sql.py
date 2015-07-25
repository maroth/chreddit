import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, DateTime, desc
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
    to_delete = session.query(Submission.id).order_by(desc(Submission.created)).offset(9500).all()
    session.commit()
    to_delete_ids = [i[0] for i in to_delete]
    if to_delete_ids:
        session.query(Submission).filter(Submission.id.in_(to_delete_ids)).delete(synchronize_session='fetch')
        session.commit()
	session.close()

def submitted(title):
    session = Session()
    result = session.query(exists().where(Submission.title==title)).scalar()
	session.close()
    return result 


 
