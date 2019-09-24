from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

def create_db(app=None):
    engine = create_engine(app.config.DB_PATH if app else 'sqlite://:memory:')
    Session = sessionmaker(bind=engine)
    return Session()

