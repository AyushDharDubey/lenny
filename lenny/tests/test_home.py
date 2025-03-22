from fastapi.testclient import TestClient
from lenny.app import app

client = TestClient(app)


def test_home():
    response = client.get("/v1/api/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello from Lenny API!",
        "status": "online"
    }
