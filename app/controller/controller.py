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

        print (f"Start: {start}, End: {end},  Data: {len(data)}")
        return data[start:end]

    @staticmethod
    async def get_classified_users(data: list, page: int, page_size: int) -> list[User]:
        filtered_users = await UserController.get_filtered_users(data)
        print(f"Filtered users count: {len(filtered_users)}") 

        paginated_users = UserController.paginate_users(filtered_users, page, page_size)
        print(f"Paginated users count: {len(paginated_users)}")

        classified_data = []
        for user in paginated_users:
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
                "birthday": user.birthday,
                "registered": user.registered,
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
            
        print(f"Classified users count: {len(classified_data)}") 
        return classified_data
        

    @staticmethod
    def classify_region(coordinates: dict) -> str:

        try:
            longitude = float(coordinates['longitude'])
            latitude = float(coordinates['latitude']) 
        except (ValueError, TypeError):
            return "trabalhoso"

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

        print(f"Longitude: {longitude}, Latitude: {latitude}")

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

            print(f"State: {state}, Region: {region}")
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
