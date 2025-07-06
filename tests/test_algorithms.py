import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app

client = TestClient(app)


class TestAlgorithms:
    @patch('app.api.deps.get_current_active_user')
    @patch('app.services.algorithm_service.AlgorithmService')
    def test_process_fibonacci(self, mock_service, mock_get_user):
        # Mock user data
        mock_user = {"id": "test-user-id", "email": "test@example.com"}
        mock_get_user.return_value = mock_user
        
        # Mock algorithm service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.process_algorithm.return_value = {
            "request_id": "test-request-id",
            "algorithm_type": "fibonacci",
            "result": {"result": 55, "sequence": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]},
            "processing_time": "calculated",
            "status": "completed"
        }
        
        # Test the endpoint
        response = client.post(
            "/api/v1/algorithms/process",
            json={
                "algorithm_type": "fibonacci",
                "input_data": {"n": 10}
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["algorithm_type"] == "fibonacci"
        assert data["result"]["result"] == 55
        assert data["status"] == "completed"
    
    @patch('app.api.deps.get_current_active_user')
    @patch('app.services.algorithm_service.AlgorithmService')
    def test_process_prime_check(self, mock_service, mock_get_user):
        # Mock user data
        mock_user = {"id": "test-user-id", "email": "test@example.com"}
        mock_get_user.return_value = mock_user
        
        # Mock algorithm service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.process_algorithm.return_value = {
            "request_id": "test-request-id",
            "algorithm_type": "prime_check",
            "result": {"is_prime": True, "number": 17},
            "processing_time": "calculated",
            "status": "completed"
        }
        
        # Test the endpoint
        response = client.post(
            "/api/v1/algorithms/process",
            json={
                "algorithm_type": "prime_check",
                "input_data": {"number": 17}
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["algorithm_type"] == "prime_check"
        assert data["result"]["is_prime"] is True
        assert data["result"]["number"] == 17
    
    @patch('app.api.deps.get_current_active_user')
    @patch('app.services.algorithm_service.AlgorithmService')
    def test_get_algorithm_history(self, mock_service, mock_get_user):
        # Mock user data
        mock_user = {"id": "test-user-id", "email": "test@example.com"}
        mock_get_user.return_value = mock_user
        
        # Mock algorithm service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.get_algorithm_history.return_value = [
            {
                "id": "request-1",
                "user_id": "test-user-id",
                "algorithm_type": "fibonacci",
                "input_data": {"n": 10},
                "result": {"result": 55},
                "status": "completed",
                "created_at": "2023-01-01T00:00:00",
                "completed_at": "2023-01-01T00:00:01"
            }
        ]
        
        # Test the endpoint
        response = client.get(
            "/api/v1/algorithms/history",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["algorithm_type"] == "fibonacci"
        assert data[0]["status"] == "completed"
    
    def test_get_algorithm_types(self):
        # Test the endpoint (no auth required)
        response = client.get("/api/v1/algorithms/types")
        
        assert response.status_code == 200
        data = response.json()
        assert "types" in data
        assert len(data["types"]) == 4  # fibonacci, prime_check, sorting, matrix_multiply
    
    def test_invalid_algorithm_type(self):
        # Test with invalid algorithm type
        response = client.post(
            "/api/v1/algorithms/process",
            json={
                "algorithm_type": "invalid_algorithm",
                "input_data": {"n": 10}
            },
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 422  # Validation error