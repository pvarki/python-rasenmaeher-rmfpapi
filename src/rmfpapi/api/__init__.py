"""Api endpoints"""
from fastapi.routing import APIRouter

from .usercrud import router as usercrud_router

all_routers = APIRouter()
all_routers.include_router(usercrud_router, prefix="/users", tags=["users"])
