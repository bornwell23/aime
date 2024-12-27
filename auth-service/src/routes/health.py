from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from common.logging import logger

from src.database import check_database_health

health_router = APIRouter()

@health_router.get("/health/check", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Comprehensive health check endpoint to verify auth service and database connectivity
    """
    # Check database health
    database_healthy = check_database_health()
    
    # Prepare health status
    health_status = {
        "status": "ok" if database_healthy else "degraded",
        "services": {
            "database": "healthy" if database_healthy else "unhealthy"
        },
        "message": "Auth service is running" + 
                   (" with all services healthy" if database_healthy else 
                    " with database connectivity issues")
    }
    
    # Log the health check
    logger.info(f'Auth service health check: {health_status}')
    
    # Set appropriate status code based on overall health
    status_code = status.HTTP_200_OK if database_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(status_code=status_code, content=health_status)
