from fastapi.testclient import TestClient


def test_borrow_book(client: TestClient):
    """Test borrowing a book via API."""
    lending_data = {
        "user_id": 1,
        "book_id": 101,
    }

    response = client.post("v1/api/lending/", json=lending_data)
    assert response.status_code == 200  # Assuming success returns 200

    data = response.json()
    assert data["user_id"] == lending_data["user_id"]
    assert data["book_id"] == lending_data["book_id"]
    assert "id" in data
