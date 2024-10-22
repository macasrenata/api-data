from fastapi import FastAPI, Depends, Query

from app.controller.controller import UserController
from app.models.schemas import PaginatedResponse
from app.services.services import DataService

app = FastAPI()

data_service = DataService()

@app.on_event("startup")
async def startup():
    await data_service.load_data()

@app.get("/api/data")
async def get_all_data(service: DataService = Depends()):
    data = await service.get_data()
    return data

@app.get("/users", response_model=PaginatedResponse)
async def get_users(service: DataService = Depends(), page: int = Query(1), page_size: int = Query(10)):
    """
    Endpoint para obter usuários elegíveis de acordo com regras de negócios.
    """
    data = await service.get_data()

    classified_users = await UserController.get_classified_users(data, page, page_size)

    total_users = len(classified_users)

    return PaginatedResponse(
        page_number=page,
        page_size=page_size,
        total_count=total_users,
        users=classified_users
    )