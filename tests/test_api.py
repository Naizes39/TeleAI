from fastapi.testclient import TestClient
from src.main import app

def test_healthy_node():
    with TestClient(app) as client:
        response = client.post("/analyze", json={
            "server_id": "string",
            "cpu_usage": 0,
            "memory_usage": 0,
            "latency_ms": 0,
            "packet_loss_percent": 0,
            "jitter_ms": 0,
            "active_network_slices": 1,
            "radio_link_failures": 0
        })
        assert response.status_code == 200
        assert response.json()['diagnostics'] is None

def test_critical_node():
    with TestClient(app) as client:
        response = client.post("/analyze", json={
            "server_id": "string",
            "cpu_usage": 100,
            "memory_usage": 100,
            "latency_ms": 0,
            "packet_loss_percent": 100,
            "jitter_ms": 80,
            "active_network_slices": 1,
            "radio_link_failures": 2
        })
        assert response.status_code == 200
        assert response.json()['diagnostics'] is not None