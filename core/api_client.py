import logging
from typing import Any, Dict, Optional
import requests

# Configure logging (basic configuration, can be overridden by pytest.ini or external config)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIClient:
    """
    Base API Client handling session management, authentication, and request logging.
    """
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        """
        Generic request method wrapping requests.Session.request with logging.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint (str): API endpoint (e.g., '/users')
            **kwargs: Additional arguments passed to requests.request
            
        Returns:
            requests.Response: Comparison response object
        """
        url = f"{self.base_url}{endpoint}"
        
        logger.info(f"REQUEST: {method.upper()} {url}")
        if 'json' in kwargs:
            logger.info(f"PAYLOAD: {kwargs['json']}")
        if 'params' in kwargs:
            logger.info(f"PARAMS: {kwargs['params']}")

        try:
            response = self.session.request(method, url, **kwargs)
            
            logger.info(f"RESPONSE STATUS: {response.status_code}")
            try:
                # content might not be json
                if response.content:
                    logger.info(f"RESPONSE BODY: {response.json()}")
                else:
                    logger.info("RESPONSE BODY: <Empty>")
            except ValueError:
                logger.info(f"RESPONSE BODY: {response.text}")
                
            return response
            
        except requests.RequestException as e:
            logger.error(f"REQUEST FAILED: {str(e)}")
            raise
