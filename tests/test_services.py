import pytest
from unittest.mock import AsyncMock, patch
from app.services.services import DataService, parse_data, parse_csv_data

@pytest.fixture
def mock_settings():
    class MockSettings:
        csv_url = "https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.csv"
        json_url = "https://storage.googleapis.com/juntossomosmais-code-challenge/input-backend.json"

    return MockSettings()

@pytest.fixture
def data_service(mock_settings):
    with patch('app.core.config.settings', mock_settings):
        service = DataService()
        return service

@pytest.fixture
def mock_user_data():
    return {
        "results": [
            {
                "gender": "male",
                "name": {
                    "title": "Mr",
                    "first": "John",
                    "last": "Doe"
                },
                "location": {
                    "coordinates": {
                        "latitude": "-23.5505",
                        "longitude": "-46.6333"
                    },
                    "state": "SP",
                    "street": "123 Main St",
                    "city": "São Paulo",
                    "timezone": {
                        "offset": "-3",
                        "description": "Brasilia"
                    }
                },
                "email": "john.doe@example.com",
                "dob": {
                    "date": "1990-01-01"
                },
                "registered": {
                    "date": "2020-01-01"
                },
                "phone": "+5511912345678",
                "cell": "+5511912345678",
                "picture": {
                    "large": "http://example.com/large.jpg",
                    "medium": "http://example.com/medium.jpg",
                    "thumbnail": "http://example.com/thumbnail.jpg"
                }
            }
        ]
    }

@pytest.mark.asyncio
async def test_load_data(data_service, mock_user_data):
    with patch('app.adapters.data_adapter.DataAdapter.fetch_and_transform_data', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.side_effect = [[], mock_user_data]
        data = await data_service.load_data()

        assert len(data) == 1
        user = data[0]
        assert user.email == "john.doe@example.com"

@pytest.mark.asyncio
async def test_get_data(data_service, mock_user_data):
    with patch('app.adapters.data_adapter.DataAdapter.fetch_and_transform_data', new_callable=AsyncMock) as mock_fetch:
        mock_fetch.side_effect = [[], mock_user_data]

        data = await data_service.get_data()

        assert len(data) == 1
        user = data[0]
        assert user.email == "john.doe@example.com"

@pytest.mark.asyncio
async def test_parse_data(mock_user_data):
    data = await parse_data(mock_user_data)

    assert len(data) == 1
    user = data[0]
    assert user.email == "john.doe@example.com"
    assert user.gender == "M"
    assert user.name.first == "John"

@pytest.mark.asyncio
async def test_parse_csv_data():
    mock_csv_content = [{
        "gender": "male",
        "name__title": "Mr",
        "name__first": "John",
        "name__last": "Doe",
        "location__coordinates__latitude": "-23.5505",
        "location__coordinates__longitude": "-46.6333",
        "location__state": "SP",
        "location__street": "123 Main St",
        "location__city": "São Paulo",
        "location__timezone__offset": "-3",
        "location__timezone__description": "Brasilia",
        "email": "john.doe@example.com",
        "dob__date": "1990-01-01",
        "registered__date": "2020-01-01",
        "phone": "+5511912345678",
        "cell": "+5511912345678",
        "picture__large": "http://example.com/large.jpg",
        "picture__medium": "http://example.com/medium.jpg",
        "picture__thumbnail": "http://example.com/thumbnail.jpg"
    }]

    data = await parse_csv_data(mock_csv_content)

    assert len(data) == 1
    user = data[0]
    assert user.email == "john.doe@example.com"
    assert user.gender == "M"
    assert user.name.first == "John"
