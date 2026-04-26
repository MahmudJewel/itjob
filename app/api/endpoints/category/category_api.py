# Update category_api.py
from fastapi import APIRouter, Depends, HTTPException
from beanie import PydanticObjectId
from typing import List

from app.schemas.category_schema import (
    CategoryCreate, CategoryUpdate, CategoryResponse,
    SubCategoryCreate, SubCategoryUpdate, SubCategoryResponse,
    TopicCreate, TopicUpdate, TopicResponse
)
from app.api.endpoints.category.category_function import (
    get_all_categories, create_category, get_category_by_id, update_category, delete_category,
    get_subcategories_by_category, create_subcategory, get_subcategory_by_id, update_subcategory, delete_subcategory,
    get_topics_by_subcategory, create_topic, get_topic_by_id, update_topic, delete_topic
)
from app.core.rolechecker import RoleChecker

# Define required roles
admin_editor_only = RoleChecker(["admin", "editor"])

category_router = APIRouter(prefix="/categories", tags=["categories"])

# =====================================> Category endpoints
@category_router.post("/", response_model=CategoryResponse)
async def create_category_endpoint(category: CategoryCreate, user=Depends(admin_editor_only)):
    category_dict = category.model_dump()
    return await create_category(category_dict)


@category_router.get("/", response_model=List[CategoryResponse])
async def get_categories():
    return await get_all_categories()


@category_router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: PydanticObjectId):
    return await get_category_by_id(category_id)


@category_router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category_endpoint(category_id: PydanticObjectId, category: CategoryUpdate, user=Depends(admin_editor_only)):
    update_dict = category.model_dump(exclude_unset=True)
    return await update_category(category_id, update_dict)


@category_router.delete("/{category_id}")
async def delete_category_endpoint(category_id: PydanticObjectId, user=Depends(admin_editor_only)):
    await delete_category(category_id)
    return {"message": "Category deleted successfully"}


# =====================================> SubCategory endpoints
subcategory_router = APIRouter(prefix="/subcategories", tags=["subcategories"])

@subcategory_router.post("/", response_model=SubCategoryResponse)
async def create_subcategory_endpoint(subcategory: SubCategoryCreate, user=Depends(admin_editor_only)):
    subcategory_dict = subcategory.model_dump()
    return await create_subcategory(subcategory_dict)


@subcategory_router.get("/category/{category_id}", response_model=List[SubCategoryResponse])
async def get_subcategories_for_category(category_id: PydanticObjectId):
    return await get_subcategories_by_category(category_id)


@subcategory_router.get("/{subcategory_id}", response_model=SubCategoryResponse)
async def get_subcategory(subcategory_id: PydanticObjectId):
    return await get_subcategory_by_id(subcategory_id)


@subcategory_router.patch("/{subcategory_id}", response_model=SubCategoryResponse)
async def update_subcategory_endpoint(subcategory_id: PydanticObjectId, subcategory: SubCategoryUpdate, user=Depends(admin_editor_only)):
    update_dict = subcategory.model_dump(exclude_unset=True)
    return await update_subcategory(subcategory_id, update_dict)


@subcategory_router.delete("/{subcategory_id}")
async def delete_subcategory_endpoint(subcategory_id: PydanticObjectId, user=Depends(admin_editor_only)):
    await delete_subcategory(subcategory_id)
    return {"message": "SubCategory deleted successfully"}


# =====================================> Topic endpoints
topic_router = APIRouter(prefix="/topics", tags=["topics"])

@topic_router.post("/", response_model=TopicResponse)
async def create_topic_endpoint(topic: TopicCreate, user=Depends(admin_editor_only)):
    topic_dict = topic.model_dump()
    return await create_topic(topic_dict)


@topic_router.get("/subcategory/{subcategory_id}", response_model=List[TopicResponse])
async def get_topics_for_subcategory(subcategory_id: PydanticObjectId):
    return await get_topics_by_subcategory(subcategory_id)


@topic_router.get("/{topic_id}", response_model=TopicResponse)
async def get_topic(topic_id: PydanticObjectId):
    return await get_topic_by_id(topic_id)


@topic_router.patch("/{topic_id}", response_model=TopicResponse)
async def update_topic_endpoint(topic_id: PydanticObjectId, topic: TopicUpdate, user=Depends(admin_editor_only)):
    update_dict = topic.model_dump(exclude_unset=True)
    return await update_topic(topic_id, update_dict)


@topic_router.delete("/{topic_id}")
async def delete_topic_endpoint(topic_id: PydanticObjectId, user=Depends(admin_editor_only)):
    await delete_topic(topic_id)
    return {"message": "Topic deleted successfully"}

