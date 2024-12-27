from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from common.logging import logger

logger.update_name("server")

# Load environment variables
load_dotenv()


def init_db():
    """Initialize the application database"""
    try:
        # Get database URL from environment
        DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://aime_admin:aime_password@localhost:5433/aime_app')

        # Create database engine
        engine = create_engine(DATABASE_URL)

        # Test connection
        with engine.connect() as conn:
            logger.info("Successfully connected to the database")

    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise


if __name__ == '__main__':
    init_db()
