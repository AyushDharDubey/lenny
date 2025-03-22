from fastapi.testclient import TestClient


def test_join_waitlist(client: TestClient):
    """Test joining the waitlist via API."""
    waitlist_data = {
        "book_id": 1,
        "user_id": 1,
    }

    response = client.post("/v1/api/waitlist/", json=waitlist_data)
    assert response.status_code == 200

    data = response.json()
    assert data["book_id"] == waitlist_data["book_id"]
    assert data["user_id"] == waitlist_data["user_id"]
    assert "id" in data
