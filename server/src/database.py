import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from typing import Optional

from common.definitions import APP_DATABASE_URL
from common.logging import logger

# Set logger name
logger.update_name("server")

# Load environment variables
load_dotenv()

# Create SQLAlchemy engine
engine = create_engine(APP_DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()


def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the application database"""
    try:
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            logger.info("Successfully connected to the database")
            return True
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False


def check_database_health(max_retries: int = 3) -> bool:
    """
    Check the health of the PostgreSQL database

    Args:
        max_retries (int): Number of times to retry the connection

    Returns:
        bool: Database health status
    """
    retry_count = 0
    while retry_count < max_retries:
        try:
            # Create a new database session
            db = SessionLocal()

            # Test the connection with a simple query
            db.execute(text("SELECT 1"))
            db.close()

            logger.info("Database connection test successful")
            return True

        except Exception as e:
            retry_count += 1
            logger.error(f"Database connection attempt {retry_count} failed: {str(e)}")

            if retry_count == max_retries:
                logger.error("Max retries reached. Database is unhealthy.")
                return False


if __name__ == "__main__":
    init_db()
