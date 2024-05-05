import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(os.environ['DATABASE_URL'])

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()