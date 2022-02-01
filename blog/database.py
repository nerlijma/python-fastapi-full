from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'
#engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={
        "check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# @contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
        # session.commit()
        
        
    except Exception as ex:
        session.rollback()
    finally:
        session.close()
