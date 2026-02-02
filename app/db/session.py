from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings

# Creating an engine entry point to the database
engine = create_engine(
    settings.database_url,
    echo=True, # show SQL queries in the console
)

# Creating new sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# Checking connection to database
def check_db_connection() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except SQLAlchemyError as e:
        print('Database connection error: ', e)
        return False