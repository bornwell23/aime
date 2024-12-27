import os
from flask import g
from common.logging import logger


class APIConfig:
    def __init__(self):
        self.server_host = os.getenv('SERVER_HOST', 'server')
        self.server_port = os.getenv('SERVER_PORT', '4000')
        self.base_url = f"http://{self.server_host}:{self.server_port}"
        self.api_version = 'v1'

        logger.info(f"API Config initialized with base URL: {self.base_url}")

    def get_api_url(self, endpoint, include_version=True):
        """
        Constructs a full API URL for the given endpoint

        Args:
            endpoint (str): The endpoint path
            include_version (bool, optional): Whether to include API version. Defaults to True.
        """
        # Remove leading slash if present
        endpoint = endpoint.lstrip('/')

        if include_version:
            return f"{self.base_url}/api/{self.api_version}/{endpoint}"
        else:
            return f"{self.base_url}/{endpoint}"

    def get_auth_headers(self):
        """
        Get headers for server API requests including roles and permissions
        """
        try:
            # Get current user from flask global context
            user = getattr(g, 'user', None)
            headers = {}

            if user:
                # Add roles and permissions headers
                if hasattr(user, 'roles'):
                    headers['X-User-Roles'] = ','.join(user.roles)
                if hasattr(user, 'permissions'):
                    headers['X-User-Permissions'] = ','.join(user.permissions)

                logger.debug(f'Added auth headers - Roles: {user.roles}, Permissions: {user.permissions}')

            return headers

        except Exception as e:
            logger.error(f'Error creating auth headers: {str(e)}')
            return {}
