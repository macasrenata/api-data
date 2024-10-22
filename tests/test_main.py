from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class MockDataService:
    async def get_data(self):
        return [
            {
                "birthday": "2000-01-01T00:00:00Z",
                "registered": "2020-01-01T00:00:00Z",
                "type": "example",
                "gender": "female",
                "name": {
                    "title": "Ms",
                    "first": "Jane",
                    "last": "Doe"
                },
                "location": {
                    "region": "SomeRegion",
                    "street": "123 Example St",
                    "city": "ExampleCity",
                    "state": "ExampleState",
                    "postcode": "12345",
                    "coordinates": {
                        "latitude": "-23.5505",
                        "longitude": "-46.6333"
                    },
                    "timezone": {
                        "offset": "-3",
                        "description": "Brasilia"
                    }
                },
                "email": "jane.doe@example.com",
                "telephone_numbers": ["+5511912345678"],
                "mobile_numbers": ["+5511912345678"],
                "picture": {
                    "large": "http://example.com/large.jpg",
                    "medium": "http://example.com/medium.jpg",
                    "thumbnail": "http://example.com/thumbnail.jpg"
                }
            }
        ]

def test_get_all_data():
    response = client.get("/api/data")
    assert response.status_code == 200
    assert len(response.json()) == 2000

def test_get_users():
    response = client.get("/api/v1/users?page=1&page_size=1")
    assert response.status_code == 200
    assert "users" in response.json()
    assert "totalCount" in response.json()

def test_get_users_invalid_page():
    response = client.get("/api/users?page=0&page_size=1")
    assert response.status_code == 404