"""
Unit and integration tests for FastAPI REST Endpoints.
"""

from fastapi.testclient import TestClient
from src.api.main import app
import src.api.main as main_module


def test_api_endpoints():
    with TestClient(app) as client:
        # Test /health
        health_resp = client.get("/health")
        assert health_resp.status_code == 200
        health_data = health_resp.json()
        assert health_data["status"] == "healthy"
        assert health_data["indexed_vectors"] >= 200

        # Test /query
        query_resp = client.post(
            "/query",
            json={"query": "What is the ESR rule for compound indexes in MongoDB?", "top_k": 3}
        )
        assert query_resp.status_code == 200
        query_data = query_resp.json()
        assert "answer" in query_data
        assert len(query_data["citations"]) > 0
        assert len(query_data["retrieved_chunks"]) > 0
        assert "latency_ms" in query_data
