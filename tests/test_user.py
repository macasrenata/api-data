from pydantic import ValidationError
import pytest
from app.models.user import UserModel
from app.models.schemas import Name, Location, Picture

@pytest.fixture
def user_data():
    return {
        "type": "example",
        "gender": "female",
        "name": Name(
            title="Ms",
            first="Jane",
            last="Doe"
        ),
        "location": Location(
            region="SomeRegion",
            street="123 Example St",
            city="ExampleCity",
            state="ExampleState",
            postcode="12345",
            coordinates={"latitude": "-23.5505", "longitude": "-46.6333"},
            timezone={"offset": "-3", "description": "Brasilia"}
        ),
        "email": "jane.doe@example.com",
        "birthday": "2000-01-01T00:00:00Z",
        "registered": "2020-01-01T00:00:00Z",
        "telephone_numbers": ["+5511912345678"],
        "mobile_numbers": ["+5511912345678"],
        "picture": Picture(
            large="http://example.com/large.jpg",
            medium="http://example.com/medium.jpg",
            thumbnail="http://example.com/thumbnail.jpg"
        ),
        "nationality": "BR"
    }

def test_user_model_creation(user_data):
    user = UserModel(**user_data)
    assert user.type == "example"
    assert user.gender == "female"
    assert user.name.first == "Jane"
    assert user.location.city == "ExampleCity"
    assert user.email == "jane.doe@example.com"
    assert user.birthday == "2000-01-01T00:00:00Z"
    assert user.registered == "2020-01-01T00:00:00Z"
    assert user.telephone_numbers == ["+5511912345678"]
    assert user.mobile_numbers == ["+5511912345678"]
    assert user.nationality == "BR"

def test_user_model_to_output(user_data):
    user = UserModel(**user_data)
    output = user.to_output()
    assert output["type"] == "example"
    assert output["gender"] == "female"
    assert output["name"]["first"] == "Jane"
    assert output["location"]["city"] == "ExampleCity"
    assert output["email"] == "jane.doe@example.com"
    assert output["birthday"] == "2000-01-01T00:00:00Z"
    assert output["registered"] == "2020-01-01T00:00:00Z"
    assert output["telephone_numbers"] == ["+5511912345678"]
    assert output["mobile_numbers"] == ["+5511912345678"]
    assert output["nationality"] == "BR"

def test_user_model_validation_invalid_email():
    with pytest.raises(ValidationError):
        UserModel(
            type="user_type",
            gender="M",
            name={"title": "Mr", "first": "John", "last": "Doe"},
            location={"region": "region", "street": "street", "city": "city", "state": "state", "postcode": "postcode", "coordinates": {"latitude": "latitude", "longitude": "longitude"}, "timezone": {"offset": "offset", "description": "description"}},
            email="invalid-email",
            birthday="1990-01-01",
            registered="2020-01-01",
            telephone_numbers=["123456789"],
            mobile_numbers=["987654321"],
            picture={"large": "url", "medium": "url", "thumbnail": "url"}
        )
