# 3rd party imports
import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from typing import Optional

from common.logging import logger

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://aime_admin:aime_password@localhost:5432/aime_auth")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

# Dependency to get database session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_database_health(max_retries: int = 3) -> bool:
    """
    Check the health of the PostgreSQL database

    :param max_retries: Number of times to retry the connection
    :return: Boolean indicating database health
    """
    for attempt in range(max_retries):
        try:
            # Create a new session
            with SessionLocal() as session:
                # Execute a simple query to check database connectivity
                result = session.execute(text("SELECT 1"))

                # If the query succeeds, the database is healthy
                logger.info("Database health check successful")
                return True
        except Exception as e:
            logger.error(f"Database health check failed (attempt {attempt + 1}): {e}")

            # Wait before retrying (you can add a delay if needed)
            if attempt < max_retries - 1:
                import time
                time.sleep(2)

    logger.error("Database health check failed after all retry attempts")
    return False
