from typing import List, Literal, Optional
from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from .common import CommonModel
from app.utils.constant.globals import QuestionType

class Option(BaseModel):
    text: str
    is_correct: bool = False


class Question(CommonModel):
    topic_id: PydanticObjectId
    created_by: Optional[PydanticObjectId] = None
    question_type: QuestionType = Field(default=[QuestionType.MCQ])
    title: str
    description: Optional[str] = None       # passage, image url, code block, etc.
    options: List[Option] = []
    answer_text: Optional[str] = None       # populated for open-ended types
    difficulty: int = Field(ge=1, le=5)

    class Settings:
        name = "questions"
