#3rd party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#project imports
from src import models
from src.database import engine
from src.logging import logger

# Import routers
from src.routes.health import health_router
from src.routes.auth import auth_router
from src.routes.user import user_router

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Aime Authentication Service")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(health_router, tags=["Health"])
app.include_router(auth_router, tags=["Authentication"])
app.include_router(user_router, tags=["Users"])