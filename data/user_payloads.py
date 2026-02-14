import uuid

# Reusable test data
test_users_data = [
    {"name": "User One", "gender": "male", "status": "active"},
    {"name": "User Two", "gender": "female", "status": "inactive"},
    {"name": "User Three", "gender": "male", "status": "active"},
]

def generate_random_email() -> str:
    """Generates a random email to avoid conflicts."""
    return f"chk_test_{uuid.uuid4().hex[:8]}@example.com"
