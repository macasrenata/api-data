import pytest
from datetime import datetime
from app.controller.controller import UserController
from app.models.user import UserModel as User

@pytest.fixture
def sample_data():
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

@pytest.mark.asyncio
async def test_get_filtered_users(sample_data):
    users = await UserController.get_filtered_users(sample_data)
    
    assert len(users) == 1
    assert isinstance(users[0], User)

def test_paginate_users(sample_data):
    users = [User(**item) for item in sample_data]
    paginated = UserController.paginate_users(users, 1, 1)
    
    assert len(paginated) == 1
    assert paginated[0].name.first == "Jane"

@pytest.mark.asyncio
async def test_get_classified_users(sample_data):
    users = await UserController.get_classified_users(sample_data, 1, 1)
    
    assert len(users) == 1
    assert users[0]["name"]["first"] == "Jane"
    assert users[0]["birthday"] == datetime.fromisoformat(sample_data[0]["birthday"][:-1]).strftime("%d/%m/%Y")

def test_classify_region():
    latitude = -23.5505
    longitude = -46.6333
    expected_result = "trabalhoso"
    assert UserController.classify_region(latitude, longitude) == expected_result

def test_classify_region_brazil():
    state = "são paulo"
    expected_result = "Sudeste"
    assert UserController.classify_region_brazil(state) == expected_result

def test_format_phone_number():
    formatted_number = UserController.format_phone_number("+5511912345678")
    
    assert formatted_number == "+55 11 91234-5678"
