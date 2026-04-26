from fastapi import APIRouter, Depends
from beanie import PydanticObjectId
from typing import List, Optional
import logging


from app.schemas.question_schema import (
    QuestionCreate, QuestionUpdate, QuestionResponse
)
from app.api.endpoints.question.question_function import (
    get_all_questions, get_question_by_id,
    create_question, update_question, delete_question,
)
from app.core.rolechecker import RoleChecker, admin_editor_only
from app.api.endpoints.user.user_function import get_current_user
from app.models.user_model import User

logger = logging.getLogger(__name__)
# admin_editor_only = RoleChecker(["admin", "editor"])

question_router = APIRouter(prefix="/questions", tags=["questions"])




@question_router.post("/", response_model=QuestionResponse, status_code=201)
async def create_question_endpoint(
    question: QuestionCreate,
    current_user: User = Depends(get_current_user)
):
    # Log the request
    # logger.info(f"Creating question with title===========> : {question.title} by user: {current_user.role}")

    # Verify user has proper role
    admin_editor_only(current_user)

    question_data = question.model_dump()
    created_question = await create_question(question_data, created_by=current_user.id)
    return created_question


@question_router.get("/", response_model=List[QuestionResponse])
async def list_questions(
    topic_id: Optional[PydanticObjectId] = None,
    question_type: Optional[str] = None,
    difficulty: Optional[int] = None,
):
    return await get_all_questions(topic_id, question_type, difficulty)


@question_router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: PydanticObjectId):
    return await get_question_by_id(question_id)


@question_router.patch("/{question_id}", response_model=QuestionResponse)
async def update_question_endpoint(
    question_id: PydanticObjectId,
    question: QuestionUpdate,
    current_user: User = Depends(get_current_user),
):
    # Verify user has proper role
    admin_editor_only(current_user)
    update_data = question.model_dump(exclude_unset=True)
    return await update_question(question_id, update_data)



@question_router.delete("/{question_id}")
async def delete_question_endpoint(
    question_id: PydanticObjectId,
    current_user: User = Depends(get_current_user),
):
    # Verify user has proper role
    admin_editor_only(current_user)
    await delete_question(question_id)
    return {"message": "Question deleted successfully"}
