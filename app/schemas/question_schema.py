# itjob/app/schemas/question_schema.py
from typing import List, Optional
from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from datetime import datetime

from app.utils.constant.globals import QuestionType


class OptionSchema(BaseModel):
    text: str
    is_correct: bool = False


class QuestionBase(BaseModel):
    topic_id: PydanticObjectId
    question_type: QuestionType  # Changed from Literal to QuestionType enum
    title: str
    description: Optional[str] = None
    options: List[OptionSchema] = []
    answer_text: Optional[str] = None
    difficulty: int = Field(ge=1, le=5)


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    topic_id: Optional[PydanticObjectId] = None
    question_type: Optional[QuestionType] = None  # Changed from Literal to QuestionType enum
    title: Optional[str] = None
    description: Optional[str] = None
    options: Optional[List[OptionSchema]] = None
    answer_text: Optional[str] = None
    difficulty: Optional[int] = Field(default=None, ge=1, le=5)


class QuestionResponse(QuestionBase):
    id: PydanticObjectId
    created_by: PydanticObjectId
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
