from fastapi import APIRouter
from temp_fastapi.api.routes import home, prediction

api_router = APIRouter()

api_router.include_router(home.router)
api_router.include_router(prediction.router)