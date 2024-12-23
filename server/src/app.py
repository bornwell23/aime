from flask import Flask
from flask_cors import CORS
import os
import time
from dotenv import load_dotenv
from api import create_api_router
from middleware.error_middleware import error_handler
from logger import logger
from utils.health_check import check_service_health, get_auth_service_health_url

# Load environment variables
load_dotenv()

def create_app():
    logger.info(' === Creating Aime Server === ')
    app = Flask(__name__)
    
    # Perform auth service health check before creating the app
    time.sleep(5)  # Wait for auth service to start
    auth_service_url = get_auth_service_health_url()
    if not check_service_health('Auth Service', auth_service_url):
        raise RuntimeError('Unable to establish connection with Auth Service')
    
    # Configure CORS
    CORS(app)
    
    # Register API routes
    api_router = create_api_router()
    app.register_blueprint(api_router, url_prefix='/api')
    
    # Register error handler
    app.register_error_handler(Exception, error_handler)
    logger.info(' === Aime Server created successfully === ')
    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 4000))
    
    logger.info(f' === Starting server on port {port} === ')
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
