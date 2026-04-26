from typing import Optional, List
from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: int = Field(default=0)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: Optional[int] = None


class CategoryResponse(CategoryBase):
    id: PydanticObjectId
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SubCategoryBase(BaseModel):
    category_id: PydanticObjectId
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: int = Field(default=0)


class SubCategoryCreate(SubCategoryBase):
    pass


class SubCategoryUpdate(BaseModel):
    category_id: Optional[PydanticObjectId] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: Optional[int] = None


class SubCategoryResponse(SubCategoryBase):
    id: PydanticObjectId
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TopicBase(BaseModel):
    sub_category_id: PydanticObjectId
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    order: int = Field(default=0)
    path: Optional[str] = None


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    sub_category_id: Optional[PydanticObjectId] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    path: Optional[str] = None


class TopicResponse(TopicBase):
    id: PydanticObjectId
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
