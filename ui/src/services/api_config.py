import os
from logger import logger

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
