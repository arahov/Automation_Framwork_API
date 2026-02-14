from typing import Dict, Any, Union
import requests
from core.api_client import APIClient

class UserService(APIClient):
    """
    Service Layer for managing User operations.
    Inherits from APIClient to reuse session and request logic.
    """
    
    def create_user(self, data: Dict[str, Any]) -> requests.Response:
        """
        Creates a new user.
        
        Args:
            data (Dict[str, Any]): User payload.
            
        Returns:
            requests.Response: API response.
        """
        return self.request("POST", "/users", json=data)

    def get_user(self, user_id: Union[int, str]) -> requests.Response:
        """
        Retrieves a user by ID.
        
        Args:
            user_id (Union[int, str]): The ID of the user.
            
        Returns:
            requests.Response: API response.
        """
        return self.request("GET", f"/users/{user_id}")

    def delete_user(self, user_id: Union[int, str]) -> requests.Response:
        """
        Deletes a user by ID.
        
        Args:
            user_id (Union[int, str]): The ID of the user.
            
        Returns:
            requests.Response: API response.
        """
        return self.request("DELETE", f"/users/{user_id}")

    def update_user(self, user_id: Union[int, str], data: Dict[str, Any]) -> requests.Response:
        """
        Updates a user by ID.
        
        Args:
            user_id (Union[int, str]): The ID of the user.
            data (Dict[str, Any]): User payload to update.
            
        Returns:
            requests.Response: API response.
        """
        return self.request("PUT", f"/users/{user_id}", json=data)
