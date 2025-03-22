from sqlmodel import Session
from fastapi.testclient import TestClient
from lenny.models import Book


def test_create_book(client: TestClient):
    """Test book creation via API."""
    book_data = {
        "title": "The Pragmatic Programmer",
        "author": "Andy Hunt & Dave Thomas",
        "isbn": "978-0201616224",
        "copies": 5,
    }

    response = client.post(
        "v1/api/books/",
        json=book_data
    )
    print(response.content)
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert data["isbn"] == book_data["isbn"]
    assert "id" in data


def test_list_books(client: TestClient, session: Session):
    """Test fetching the book list."""

    book = Book(
        title="Clean Code",
        author="Robert C. Martin",
        isbn="978-0132350884",
        available_copies=5,
        total_copies=5,
    )
    session.add(book)
    session.commit()
    session.refresh(book)

    response = client.get("v1/api/books/")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Clean Code"
    assert data[0]["author"] == "Robert C. Martin"
    assert data[0]["isbn"] == "978-0132350884"
