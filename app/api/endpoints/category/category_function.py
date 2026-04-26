from typing import List, Optional
from beanie import PydanticObjectId
from fastapi import HTTPException, status
from slugify import slugify
from typing import Dict, Any

from app.models import Category, SubCategory, Topic





# Category functions
async def get_category_by_id(category_id: PydanticObjectId) -> Category:
    category = await Category.find_one(Category.id == category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


async def get_category_by_slug(slug: str) -> Category:
    category = await Category.find_one(Category.slug == slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


async def get_all_categories() -> List[Category]:
    return await Category.find_all().sort([("order", 1), ("name", 1)]).to_list()



async def create_category(category_data: Dict[str, Any]) -> Category:
    # If slug is not provided, generate it from name
    if not category_data.get('slug'):
        name = category_data.get('name', '')
        # Generate slug from name
        slug = slugify(name, separator='-')
        
        # Check if slug already exists and make it unique
        existing_category = await Category.find_one({"slug": slug})
        if existing_category:
            # Append a number to make it unique
            counter = 1
            while True:
                new_slug = f"{slug}-{counter}"
                existing_category = await Category.find_one({"slug": new_slug})
                if not existing_category:
                    slug = new_slug
                    break
                counter += 1
        
        category_data['slug'] = slug
    
    category = Category(**category_data)
    await category.insert()
    return category


async def update_category(category_id: PydanticObjectId, update_data: dict) -> Category:
    category = await get_category_by_id(category_id)
    for key, value in update_data.items():
        if value is not None:
            setattr(category, key, value)
    await category.save()
    return category


async def delete_category(category_id: PydanticObjectId) -> None:
    category = await get_category_by_id(category_id)
    await category.delete()


# SubCategory functions
async def get_subcategory_by_id(subcategory_id: PydanticObjectId) -> SubCategory:
    subcategory = await SubCategory.find_one(SubCategory.id == subcategory_id)
    if not subcategory:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return subcategory


async def get_subcategory_by_slug(slug: str) -> SubCategory:
    subcategory = await SubCategory.find_one(SubCategory.slug == slug)
    if not subcategory:
        raise HTTPException(status_code=404, detail="SubCategory not found")
    return subcategory


async def get_subcategories_by_category(category_id: PydanticObjectId) -> List[SubCategory]:
    return await SubCategory.find(SubCategory.category_id == category_id).sort([("order", 1), ("name", 1)]).to_list()


async def create_subcategory(subcategory_data: dict) -> SubCategory:
    # Verify category exists
    await get_category_by_id(subcategory_data["category_id"])
    
    # If slug is not provided, generate it from name
    if not subcategory_data.get('slug'):
        name = subcategory_data.get('name', '')
        # Generate slug from name
        slug = slugify(name, separator='-')
        
        # Check if slug already exists and make it unique
        existing_subcategory = await SubCategory.find_one({"slug": slug})
        if existing_subcategory:
            # Append a number to make it unique
            counter = 1
            while True:
                new_slug = f"{slug}-{counter}"
                existing_subcategory = await SubCategory.find_one({"slug": new_slug})
                if not existing_subcategory:
                    slug = new_slug
                    break
                counter += 1
        
        subcategory_data['slug'] = slug
    
    subcategory = SubCategory(**subcategory_data)
    await subcategory.insert()
    return subcategory


async def update_subcategory(subcategory_id: PydanticObjectId, update_data: dict) -> SubCategory:
    subcategory = await get_subcategory_by_id(subcategory_id)
    if "category_id" in update_data and update_data["category_id"] is not None:
        await get_category_by_id(update_data["category_id"])
    
    # Handle slug update if provided
    if 'slug' in update_data and update_data['slug'] is not None:
        if not update_data['slug']:  # If slug is empty
            name = update_data.get('name', '') or subcategory.name
            slug = slugify(name, separator='-')
            
            # Check if slug already exists and make it unique
            existing_subcategory = await SubCategory.find_one({"slug": slug})
            if existing_subcategory:
                counter = 1
                while True:
                    new_slug = f"{slug}-{counter}"
                    existing_subcategory = await SubCategory.find_one({"slug": new_slug})
                    if not existing_subcategory:
                        slug = new_slug
                        break
                    counter += 1
            update_data['slug'] = slug
    
    for key, value in update_data.items():
        if value is not None:
            setattr(subcategory, key, value)
    await subcategory.save()
    return subcategory


async def delete_subcategory(subcategory_id: PydanticObjectId) -> None:
    subcategory = await get_subcategory_by_id(subcategory_id)
    await subcategory.delete()


# Topic functions
async def get_topic_by_id(topic_id: PydanticObjectId) -> Topic:
    topic = await Topic.find_one(Topic.id == topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


async def get_topic_by_slug(slug: str) -> Topic:
    topic = await Topic.find_one(Topic.slug == slug)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


async def get_topics_by_subcategory(subcategory_id: PydanticObjectId) -> List[Topic]:
    return await Topic.find(Topic.sub_category_id == subcategory_id).sort([("order", 1), ("name", 1)]).to_list()


async def create_topic(topic_data: dict) -> Topic:
    # Verify subcategory exists
    await get_subcategory_by_id(topic_data["sub_category_id"])
    
    # If slug is not provided, generate it from name
    if not topic_data.get('slug'):
        name = topic_data.get('name', '')
        # Generate slug from name
        slug = slugify(name, separator='-')
        
        # Check if slug already exists and make it unique
        existing_topic = await Topic.find_one({"slug": slug})
        if existing_topic:
            # Append a number to make it unique
            counter = 1
            while True:
                new_slug = f"{slug}-{counter}"
                existing_topic = await Topic.find_one({"slug": new_slug})
                if not existing_topic:
                    slug = new_slug
                    break
                counter += 1
        
        topic_data['slug'] = slug
    
    topic = Topic(**topic_data)
    await topic.insert()
    return topic


async def update_topic(topic_id: PydanticObjectId, update_data: dict) -> Topic:
    topic = await get_topic_by_id(topic_id)
    if "sub_category_id" in update_data and update_data["sub_category_id"] is not None:
        await get_subcategory_by_id(update_data["sub_category_id"])
    
    # Handle slug update if provided
    if 'slug' in update_data and update_data['slug'] is not None:
        if not update_data['slug']:  # If slug is empty
            name = update_data.get('name', '') or topic.name
            slug = slugify(name, separator='-')
            
            # Check if slug already exists and make it unique
            existing_topic = await Topic.find_one({"slug": slug})
            if existing_topic:
                counter = 1
                while True:
                    new_slug = f"{slug}-{counter}"
                    existing_topic = await Topic.find_one({"slug": new_slug})
                    if not existing_topic:
                        slug = new_slug
                        break
                    counter += 1
            update_data['slug'] = slug
    
    for key, value in update_data.items():
        if value is not None:
            setattr(topic, key, value)
    await topic.save()
    return topic


async def delete_topic(topic_id: PydanticObjectId) -> None:
    topic = await get_topic_by_id(topic_id)
    await topic.delete()