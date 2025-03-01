from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

def init_db(db_url='sqlite:///students.db'):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
