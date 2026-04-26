from typing import List, Optional, Dict, Any
from beanie import PydanticObjectId
from fastapi import HTTPException

from app.models import Question
from app.models.category_model import Topic


# ==============================================> Helpers

async def _verify_topic(topic_id: PydanticObjectId) -> None:
    topic = await Topic.find_one(Topic.id == topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")


async def get_question_by_id(question_id: PydanticObjectId) -> Question:
    question = await Question.find_one(Question.id == question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


# ==============================================> CRUD

async def get_all_questions(
    topic_id: Optional[PydanticObjectId] = None,
    question_type: Optional[str] = None,
    difficulty: Optional[int] = None,
) -> List[Question]:
    query = {}
    if topic_id:
        query["topic_id"] = topic_id
    if question_type:
        query["question_type"] = question_type
    if difficulty is not None:
        query["difficulty"] = difficulty
    return await Question.find(query).sort([("difficulty", 1)]).to_list()


async def create_question(
    question_data: Dict[str, Any],
    created_by: PydanticObjectId,
) -> Question:
    await _verify_topic(question_data["topic_id"])
    question_data["created_by"] = created_by
    question = Question(**question_data)
    await question.insert()
    return question


async def update_question(
    question_id: PydanticObjectId,
    update_data: Dict[str, Any],
) -> Question:
    question = await get_question_by_id(question_id)

    if "topic_id" in update_data and update_data["topic_id"] is not None:
        await _verify_topic(update_data["topic_id"])

    for key, value in update_data.items():
        if value is not None:
            setattr(question, key, value)

    await question.save()
    return question


async def delete_question(question_id: PydanticObjectId) -> None:
    question = await get_question_by_id(question_id)
    await question.delete()
