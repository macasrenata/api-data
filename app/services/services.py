from app.adapters.data_adapter import DataAdapter
from app.models.user import UserModel as User
from app.models.schemas import Name, Location, Picture
from app.controller.controller import UserController
from app.core.config import settings

user_data = UserController()

class DataService:
    def __init__(self):
        self._data_cache = None
        self.settings = settings

    async def load_data(self):
        if not self._data_cache:
            csv_url = self.settings.csv_url
            json_url = self.settings.json_url

            csv_content = await DataAdapter.fetch_and_transform_data(csv_url, "csv")
            json_content = await DataAdapter.fetch_and_transform_data(json_url, "json")

            data_json = await parse_data(json_content)
            data_csv = await parse_csv_data(csv_content)

            self._data_cache = data_json + data_csv

        return self._data_cache

    async def get_data(self):
        return await self.load_data()

async def parse_data(json_content: list[dict]) -> list[User]:
    """
    Função para converter dados CSV e JSON em uma lista de objetos UserModel.
    
    :param json_content: Conteúdo JSON como string.
    :return: lista de UserModel.
    """
    parsed_data = []

    if 'results' in json_content:
        for user in json_content["results"]:
            user_model = User(
                type=user_data.classify_region(user["location"]["coordinates"]["latitude"], user["location"]["coordinates"]["longitude"]),
                gender="M" if user["gender"] == "male" else "F",
                name=Name(
                    title=user["name"]["title"],
                    first=user["name"]["first"],
                    last=user["name"]["last"]
                ),
                location=Location(
                    region= user_data.classify_region_brazil(user["location"]["state"]),
                    street=user["location"]["street"],
                    city=user["location"]["city"],
                    state=user["location"]["state"],
                    postcode=user["location"].get("postcode", ""),
                    coordinates={
                        "latitude": user["location"]["coordinates"]["latitude"],
                        "longitude": user["location"]["coordinates"]["longitude"]
                    },
                    timezone={
                        "offset": user["location"]["timezone"]["offset"],
                        "description": user["location"]["timezone"]["description"]
                    }
                ),
                email=user["email"],
                birthday=user["dob"]["date"],
                registered=user["registered"]["date"],
                telephone_numbers=[user_data.format_phone_number(user["phone"])],
                mobile_numbers=[user_data.format_phone_number(user["cell"])],
                picture=Picture(
                    large=user["picture"]["large"],
                    medium=user["picture"]["medium"],
                    thumbnail=user["picture"]["thumbnail"]
                ),
                nationality=user.get("nationality", "BR")
            )
            parsed_data.append(user_model)

    return parsed_data

async def parse_csv_data(csv_content: list[dict]) -> list[User]:
    """
    Função para converter dados CSV em uma lista de objetos UserModel.
    
    :param csv_content: Conteúdo bruto do CSV como string.
    :return: lista de UserModel.
    """
    parsed_data = []

    for row in csv_content:
        user_model = User(
            type=user_data.classify_region(row.get("location__coordinates__latitude", ""), row.get("location__coordinates__longitude", "")),
            gender="M" if row["gender"] == "male" else "F",
            name=Name(
                title=row.get("name__title", ""),
                first=row.get("name__first", ""),
                last=row.get("name__last", "")
            ),
            location=Location(
                region=user_data.classify_region_brazil(row.get("location__state", "")),
                street=row.get("location__street", ""),
                city=row.get("location__city", ""),
                state=row.get("location__state", ""),
                postcode=row.get("location__postcode", ""),
                coordinates={
                    "latitude": row.get("location__coordinates__latitude", ""),
                    "longitude": row.get("location__coordinates__longitude", "")
                },
                timezone={
                    "offset": row.get("location__timezone__offset", ""),
                    "description": row.get("location__timezone__description", "")
                }
            ),
            email=row.get("email", ""),
            birthday=row.get("dob__date", ""),
            registered=row.get("registered__date", ""),
            telephone_numbers=[user_data.format_phone_number(row.get("phone", ""))],
            mobile_numbers=[user_data.format_phone_number(row.get("cell", ""))],
            picture=Picture(
                large=row.get("picture__large", ""),
                medium=row.get("picture__medium", ""),
                thumbnail=row.get("picture__thumbnail", "")
            ),
            nationality=row.get("nationality", "BR") or "BR"
        )
        parsed_data.append(user_model)

    return parsed_data