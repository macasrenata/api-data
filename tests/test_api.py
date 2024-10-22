from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_users():
    response = client.get("/api/v1/users?page=1&page_size=10")
    assert response.status_code == 200
    assert "pageNumber" in response.json()
    assert "users" in response.json()
