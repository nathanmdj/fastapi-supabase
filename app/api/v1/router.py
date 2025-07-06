from fastapi import APIRouter

from app.api.v1 import auth, algorithms

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(algorithms.router, prefix="/algorithms", tags=["Algorithms"])