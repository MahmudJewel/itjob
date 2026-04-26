from fastapi import APIRouter
from app.api.endpoints.question.question_api import question_router

question_main_router = APIRouter()
question_main_router.include_router(question_router)
