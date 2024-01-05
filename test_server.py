from fastapi.testclient import TestClient
from server import app, ROUTE_SERVER_STATUS, ServerStatus
import pytest


@pytest.fixture
def client():
    return TestClient(app)

def test_status(client):
    response = client.get(ROUTE_SERVER_STATUS)
    server_status = ServerStatus.model_validate(response.json())
    assert response.status_code == 200
    assert server_status == ServerStatus(status=True)
