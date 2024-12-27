import os
import requests
import time
from common.logging import logger


def check_service_health(service_name, service_url, max_retries=3, delay=5):
    """
    Perform health check on a service with retry mechanism

    :param service_name: Name of the service for logging
    :param service_url: Full URL of the health check endpoint
    :param max_retries: Maximum number of retry attempts
    :param delay: Delay between retry attempts in seconds
    :return: Boolean indicating service health
    """
    for attempt in range(max_retries):
        logger.info(f'{service_name} health check attempt {attempt + 1} of {max_retries}')
        try:
            response = requests.get(service_url, timeout=5)
            # Check for 200 status code and optional JSON response
            if response.status_code == 200:
                # Optional: Check for expected JSON structure if needed
                response_data = response.json()
                if response_data.get('status') == 'ok':
                    logger.info(f'{service_name} health check successful')
                    return True
                logger.warning(f'{service_name} health check returned unexpected response')
            else:
                logger.warning(f'{service_name} health check failed. Status code: {response.status_code}')
        except requests.exceptions.RequestException as e:
            logger.error(f'{service_name} health check error (attempt {attempt + 1}): {e}')
        except ValueError:  # JSON decoding error
            logger.error(f'{service_name} health check returned invalid JSON')

        # Wait before retrying
        time.sleep(delay)

    logger.error(f'{service_name} health check failed after maximum retries')
    return False


def get_auth_service_health_url():
    """
    Construct the health check URL for the auth service
    """
    host = os.getenv('AUTH_SERVICE_HOST', 'auth-service')
    port = os.getenv('AUTH_SERVICE_PORT', '8000')
    return f'http://{host}:{port}/health/check'
