import pytest
import os
from dotenv import load_dotenv
from services.user_service import UserService

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope="session")
def auth_token():
    """Returns the authentication token from env."""
    token = os.getenv("GOREST_TOKEN")
    if not token:
        pytest.fail("GOREST_TOKEN not found in environment variables or .env file.")
    return token

@pytest.fixture(scope="session")
def base_url():
    """Returns the base URL for GoRest API."""
    return "https://gorest.co.in/public/v2"

@pytest.fixture(scope="session")
def user_service(base_url, auth_token):
    """Initializes the UserService with base URL and token."""
    return UserService(base_url, auth_token)
