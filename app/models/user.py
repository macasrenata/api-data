from pydantic import BaseModel
from app.models.schemas import Name, Location, Picture

class UserModel(BaseModel):
    type: str
    gender: str
    name: Name
    location: Location
    email: str
    birthday: str
    registered: str
    telephone_numbers: list[str]
    mobile_numbers: list[str]
    picture: Picture
    nationality: str = "BR"

    def to_output(self):
        return self.model_dump()
