import pytest
from data.user_payloads import generate_random_email

class TestUserEdgeCases:
    """
    Edge case tests for User operations.
    """

    def test_create_user_duplicate_email(self, user_service):
        """
        Test creating a user with an email that already exists.
        
        Given: A created user
        When: I try to create another user with the same email
        Then: The response status should be 422
        And: The error message should comply "has already been taken"
        """
        # 1. Create first user
        email = generate_random_email()
        payload = {
            "name": "Original User",
            "gender": "male",
            "email": email,
            "status": "active"
        }
        res1 = user_service.create_user(payload)
        assert res1.status_code == 201

        # 2. Try to create second user with same email
        payload_duplicate = {
            "name": "Duplicate User",
            "gender": "female",
            "email": email,
            "status": "inactive"
        }
        res2 = user_service.create_user(payload_duplicate)
        
        # 3. Verify failure
        assert res2.status_code == 422
        errors = res2.json()
        email_error = next((e for e in errors if e["field"] == "email"), None)
        assert email_error is not None
        assert "has already been taken" in email_error["message"]

    @pytest.mark.parametrize("invalid_gender", ["batman", ""])
    def test_create_user_invalid_gender(self, user_service, invalid_gender):
        """
        Test creating a user with invalid gender values.
        
        Given: A payload with invalid gender
        When: I send a POST request
        Then: The response status should be 422
        """
        payload = {
            "name": "Invalid Gender User",
            "gender": invalid_gender,
            "email": generate_random_email(),
            "status": "active"
        }
        response = user_service.create_user(payload)
        assert response.status_code == 422
        
        errors = response.json()
        assert any(e["field"] == "gender" for e in errors)

    def test_create_user_max_length_fields(self, user_service):
        """
        Test creating a user with extremely long name.
        Note: GoRest might truncate or allow it, but we check for 201 or specific behavior.
        Assuming generous limit, but let's test a reasonable boundary.
        """
        long_name = "A" * 256 # Typically APIs cap at 255 or similar
        payload = {
            "name": long_name,
            "gender": "male",
            "email": generate_random_email(),
            "status": "active"
        }
        response = user_service.create_user(payload)
        
        # If the API allows it, 201. If strict, 422.
        # We will log the behavior. For now, let's assert it handles it gracefully (not 500).
        assert response.status_code in [201, 422] 

    def test_update_user_empty_body(self, user_service):
        """
        Test updating a user with an empty body.
        
        Given: A created user
        When: I send a PUT request with empty JSON
        Then: The response should be 200 (idempotent/no-op) or 204
        """
        # Create
        payload = {
            "name": "Empty Update User",
            "gender": "male",
            "email": generate_random_email(),
            "status": "active"
        }
        create_res = user_service.create_user(payload)
        user_id = create_res.json()["id"]

        # Update Empty
        update_res = user_service.update_user(user_id, {})
        assert update_res.status_code == 200
        # Ensure fields didn't change (e.g. name remains)
        assert update_res.json()["name"] == "Empty Update User"

    def test_delete_user_not_found(self, user_service):
        """
        Test deleting a user that doesn't exist.
        
        Given: A non-existent user ID
        When: I send a DELETE request
        Then: The response should be 404
        """
        response = user_service.delete_user(99999999)
        assert response.status_code == 404
