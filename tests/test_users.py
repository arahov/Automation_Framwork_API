import pytest
from data.user_payloads import test_users_data, generate_random_email

class TestUsers:
    """
    Test suite for User API endpoints.
    """

    @pytest.mark.regression
    @pytest.mark.parametrize("user_data", test_users_data)
    def test_create_user_success(self, user_service, user_data):
        """
        Test creating a user with valid data.
        
        Given: A valid user payload
        When: I send a POST request to /users
        Then: The response status code should be 201
        And: The response body should contain the created user data
        """
        # Prepare payload with unique email
        payload = user_data.copy()
        payload["email"] = generate_random_email()
        
        response = user_service.create_user(payload)
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        data = response.json()
        assert data["name"] == payload["name"]
        assert data["email"] == payload["email"]
        assert data["gender"] == payload["gender"]
        assert data["status"] == payload["status"]
        assert "id" in data

    @pytest.mark.parametrize("invalid_email", [
        "invalid-email",
        "missing_at_symbol.com",
        "missing_domain@",
        "@missing_username.com",
        "spaces in email@example.com"
    ])
    def test_create_user_invalid_email(self, user_service, invalid_email):
        """
        Test creating a user with various invalid email formats.
        
        Given: A payload with an invalid email
        When: I send a POST request to /users
        Then: The response status code should be 422
        """
        payload = {
            "name": "Invalid Email User",
            "gender": "male",
            "email": invalid_email,
            "status": "active"
        }
        
        response = user_service.create_user(payload)
        
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"
        errors = response.json()
        email_errors = [e for e in errors if e.get("field") == "email"]
        assert len(email_errors) > 0, "Expected error for 'email' field"

    @pytest.mark.smoke
    def test_full_user_lifecycle(self, user_service):
        """
        Test the full lifecycle of a user: Create -> Get -> Delete.
        
        Given: A new user payload
        When: I create the user
        Then: The user should be created successfully (201)
        
        When: I retrieve the user by ID
        Then: The user details should match the created user (200)
        
        When: I delete the user
        Then: The user should be deleted successfully (204)
        
        When: I try to retrieve the deleted user
        Then: The response status should be 404
        """
        # 1. Create
        payload = {
            "name": "Lifecycle User",
            "gender": "female",
            "email": generate_random_email(),
            "status": "active"
        }
        create_response = user_service.create_user(payload)
        assert create_response.status_code == 201
        user_id = create_response.json()["id"]
        
        # 2. Get
        get_response = user_service.get_user(user_id)
        assert get_response.status_code == 200
        assert get_response.json()["id"] == user_id
        
        # 3. Delete
        delete_response = user_service.delete_user(user_id)
        assert delete_response.status_code == 204
        
        # 4. Verify Delete
        get_after_delete = user_service.get_user(user_id)
        assert get_after_delete.status_code == 404

    @pytest.mark.parametrize("update_field, update_value", [
        ("name", "Updated Param Name"),
        ("email", generate_random_email()),
        ("status", "inactive")
    ])
    def test_update_user_fields(self, user_service, update_field, update_value):
        """
        Test updating various user fields.
        
        Given: A created user
        When: I update a specific field
        Then: The response status should be 200
        And: The field should be updated in the response
        """
        # Create
        payload = {
            "name": "Update Test User",
            "gender": "male",
            "email": generate_random_email(),
            "status": "active"
        }
        create_res = user_service.create_user(payload)
        user_id = create_res.json()["id"]

        # Update
        update_payload = {update_field: update_value}
        update_res = user_service.update_user(user_id, update_payload)
        assert update_res.status_code == 200
        assert update_res.json()[update_field] == update_value

        # Verify Get
        get_res = user_service.get_user(user_id)
        assert get_res.json()[update_field] == update_value

    def test_get_non_existent_user(self, user_service):
        """
        Test retrieving a non-existent user.
        
        Given: An invalid user ID
        When: I request the user details
        Then: The response status should be 404
        """
        response = user_service.get_user(99999999) # Using a very large ID
        assert response.status_code == 404

    @pytest.mark.parametrize("missing_field", ["name", "email", "gender", "status"])
    def test_create_user_missing_fields(self, user_service, missing_field):
        """
        Test creating a user with missing required fields.
        
        Given: A payload missing a required field
        When: I send a POST request to /users
        Then: The response status should be 422
        And: The error message should indicate the missing field
        """
        payload = {
            "name": "Missing Field User",
            "gender": "female",
            "email": generate_random_email(),
            "status": "active"
        }
        del payload[missing_field]
        
        response = user_service.create_user(payload)
        assert response.status_code == 422
        
        errors = response.json()
        field_errors = [e for e in errors if e.get("field") == missing_field]
        assert len(field_errors) > 0, f"Expected error for missing field '{missing_field}'"
