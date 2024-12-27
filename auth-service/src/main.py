#3rd party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from common.logging import logger

# Configure logging
logger.update_name("auth-service")

#project imports
from src import models
from src.database import engine, check_database_health

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="Aime Authentication Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Import routers
from src.routes.health import health_router
from src.routes.auth import auth_router
from src.routes.user import user_router

# Include routers
app.include_router(health_router, tags=["Health"])
app.include_router(auth_router, tags=["Authentication"])
app.include_router(user_router, tags=["Users"])

try:
    # Perform database connection check
    check_database_health()
    logger.info("Auth service startup completed successfully")
except Exception as e:
    logger.error(f"Auth service startup failed: {e}")
    raise