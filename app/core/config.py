from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    csv_url: str
    json_url: str
    api_base_url: str = "http://localhost:8080/api"

    class Config:
        env_file = ".env"

settings = Settings()
