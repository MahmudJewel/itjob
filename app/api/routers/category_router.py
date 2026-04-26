from fastapi import APIRouter
from app.api.endpoints.category.category_api import category_router, subcategory_router, topic_router

category_main_router = APIRouter()

category_main_router.include_router(category_router)
category_main_router.include_router(subcategory_router)
category_main_router.include_router(topic_router)