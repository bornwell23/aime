from routes.history import register_history_routes
from routes.auth import register_auth_routes
from routes.pages import register_main_routes
from services.api_config import APIConfig
from services.account import AccountManager
from flask import Flask
from flask_login import LoginManager
import os
from dotenv import load_dotenv
import time

from common.logging import logger

logger.update_name("ui")


# Import route registration functions

# Load environment variables
load_dotenv()


def check_server_health(max_retries=3, delay=5):
    """
    Perform health check on the server with retry mechanism
    """
    api_config = APIConfig()
    health_url = api_config.get_api_url('/health/check')

    for attempt in range(max_retries):
        try:
            import requests
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                logger.info('Server health check successful')
                return True
            logger.warning(f'Health check failed. Status code: {response.status_code}')
        except requests.RequestException as e:
            logger.error(f'Health check error (attempt {attempt + 1}): {e}')

        # Wait before retrying
        time.sleep(delay)

    logger.error('Server health check failed after maximum retries')
    return False


def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

    # Perform server health check before creating the app
    time.sleep(5)  # Wait for services to start
    if not check_server_health():
        raise RuntimeError('Unable to establish connection with server')

    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        """
        Callback to reload the user object from the user ID stored in the session
        """
        try:

            logger.info(f"Loading user with ID: {user_id}")
            return AccountManager().get_user(user_id)
        except Exception as e:
            logger.error(f"Error loading user: {e}")
            return None

    # Register routes
    register_main_routes(app)
    register_auth_routes(app)
    register_history_routes(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3000)), debug=True)
