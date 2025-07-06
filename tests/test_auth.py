import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app

client = TestClient(app)


class TestAuth:
    @patch('app.api.deps.get_current_user')
    def test_get_current_user_info(self, mock_get_user):
        # Mock user data
        mock_user = {
            "id": "test-user-id",
            "email": "test@example.com",
            "email_confirmed_at": "2023-01-01T00:00:00",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00",
            "user_metadata": {}
        }
        mock_get_user.return_value = mock_user
        
        # Test the endpoint
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["id"] == "test-user-id"
    
    @patch('app.api.deps.get_current_user')
    def test_verify_token(self, mock_get_user):
        # Mock user data
        mock_user = {
            "id": "test-user-id",
            "email": "test@example.com"
        }
        mock_get_user.return_value = mock_user
        
        # Test the endpoint
        response = client.post(
            "/api/v1/auth/verify-token",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert data["user_id"] == "test-user-id"
        assert data["email"] == "test@example.com"
    
    def test_unauthorized_access(self):
        # Test without authorization header
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 403  # FastAPI security dependency returns 403
    
    def test_invalid_token(self):
        # Test with invalid token
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid-token"}
        )
        assert response.status_code == 401