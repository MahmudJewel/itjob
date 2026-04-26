from typing import Optional
from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field

from .common import CommonModel


class Category(CommonModel):
    name: str
    slug: Indexed(str, unique=True)
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: int = Field(default=0)  # for sorting

    class Settings:
        name = "categories"


class SubCategory(CommonModel):
    category_id: PydanticObjectId
    name: str
    slug: Indexed(str, unique=True)
    description: Optional[str] = None
    image_url: Optional[str] = None
    order: int = Field(default=0)

    class Settings:
        name = "sub_categories"


class Topic(CommonModel):
    sub_category_id: PydanticObjectId
    name: str
    slug: Indexed(str, unique=True)
    description: Optional[str] = None
    order: int = Field(default=0)
    # Materialized path for fast breadcrumb/search
    path: Optional[str] = None  # e.g. "Math / Algebra / Quadratic Equations"

    class Settings:
        name = "topics"