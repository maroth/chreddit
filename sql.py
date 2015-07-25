import os, config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer, DateTime, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists 

engine = create_engine(config.database_url)
Session = sessionmaker()
Session.configure(bind=engine)

Base = declarative_base()
class Submission(Base):
    __tablename__ = config.tablename
    id = Column(Integer, primary_key=True)
    title = Column(String)
    created = Column(DateTime)

Base.metadata.create_all(engine)

def submit(title):
    submission = Submission(title=title)
    session = Session()
    session.add(submission)
    session.commit()

    #free database in heroku is limited, so delete old ones
    to_delete = session.query(Submission.id).order_by(desc(Submission.created)).offset(config.max_rows).all()
    session.commit()
    to_delete_ids = [i[0] for i in to_delete]
    if to_delete_ids:
        print 'deleting ' + str(len(to_delete_ids)) + ' items from database'
        session.query(Submission).filter(Submission.id.in_(to_delete_ids)).delete(synchronize_session='fetch')
        session.commit()
	session.close()

def submitted(title):
    session = Session()
    result = session.query(exists().where(Submission.title==title)).scalar()
    session.close()
    return result 


 
