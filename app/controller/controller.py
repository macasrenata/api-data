from datetime import datetime
import phonenumbers
from app.models.user import UserModel as User

from app.utils.utils import REGIONS_MAP

class UserController:

    @staticmethod
    async def get_filtered_users(data: list) -> list[User]:

        users = []
        for item in data:
            user_data = item.model_dump()
            user = User(**user_data)
            users.append(user)
        return users

    @staticmethod
    def paginate_users(data: list[User], page: int, page_size: int) -> list[User]:
        start = (page - 1) * page_size
        end = start + page_size

        return data[start:end]

    @staticmethod
    async def get_classified_users(data: list, page: int, page_size: int) -> list[User]:
        filtered_users = await UserController.get_filtered_users(data)

        paginated_users = UserController.paginate_users(filtered_users, page, page_size)

        classified_data = []
        for user in paginated_users:
            birthday = datetime.fromisoformat(user.birthday[:-1]).strftime("%d/%m/%Y")  # Formato "dia/mês/ano"
            registered = datetime.fromisoformat(user.registered[:-1]).strftime("%d/%m/%Y")  # Formato "dia/mês/ano"
            classified_user = {
                "type": user.type,
                "gender": user.gender,
                "name": {
                    "title": user.name.title,
                    "first": user.name.first,
                    "last": user.name.last
                },
                "location": {
                    "region": user.location.region,
                    "street": user.location.street,
                    "city": user.location.city,
                    "state": user.location.state,
                    "postcode": user.location.postcode,
                    "coordinates": {
                        "latitude": user.location.coordinates.latitude,
                        "longitude": user.location.coordinates.longitude
                    },
                    "timezone": {
                        "offset": user.location.timezone.offset,
                        "description": user.location.timezone.description
                    }
                },
                "email": user.email,
                "birthday": birthday,
                "registered": registered,
                "telephone_numbers": user.telephone_numbers,
                "mobile_numbers": user.mobile_numbers,
                "picture": {
                    "large": user.picture.large,
                    "medium": user.picture.medium,
                    "thumbnail": user.picture.thumbnail
                }, 
                "nationality": "BR",
            }
            classified_data.append(classified_user)
            
        return classified_data
        

    @staticmethod
    def classify_region(latitude: str, longitude: str) -> str:

        longitude = float(longitude)
        latitude = float(latitude) 

        especial_box = {
            "minlon": -15.411580,
            "minlat": -52.997614,
            "maxlon": -2.196998,
            "maxlat": -34.276938
        }

        normal_box = {
            "minlon": -34.016466,
            "minlat": -54.777426,
            "maxlon": -26.155681,
            "maxlat": -46.603598
        }

        if (especial_box["minlon"] <= longitude <= especial_box["maxlon"] and
                    especial_box["minlat"] <= latitude <= especial_box["maxlat"]):
                return "especial"
            
        if (normal_box["minlon"] <= longitude <= normal_box["maxlon"] and
                    normal_box["minlat"] <= latitude <= normal_box["maxlat"]):
                return "normal"

        return "trabalhoso"
    
    @staticmethod
    def classify_region_brazil(state: str) -> str:

        if state:
            region = REGIONS_MAP.get(state)

            if region:
                return region
            else:
                return "Estado não encontrado"
        else:
            return "Região não encontrada"
        
    
    @staticmethod
    def format_phone_number(number: str) -> dict:
        parsed_number = phonenumbers.parse(number, "BR")
    
        international_format = phonenumbers.format_number(
            parsed_number, 
            phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
        
        return international_format
