from typing import Optional
from pydantic import BaseModel

class Coordinates(BaseModel):
    latitude: str
    longitude: str

class Timezone(BaseModel):
    offset: str
    description: str

class Location(BaseModel):
    region: str
    street: str
    city: str
    state: str
    postcode: int
    coordinates: Coordinates
    timezone: Timezone

class Name(BaseModel):
    title: str
    first: str
    last: str

class Picture(BaseModel):
    large: str
    medium: str
    thumbnail: str

class User(BaseModel):
    gender: str
    name: Name
    location: Location
    email: str
    birthday: Optional[str]
    registered: Optional[str]
    telephone_numbers: list[str]
    mobile_numbers: list[str]
    picture: Picture
    nationality: str

class PaginatedResponse(BaseModel):
    page_number: int
    page_size: int
    total_count: int
    users: list[User]
