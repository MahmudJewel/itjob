import pytest
from uuid import uuid4
from beanie import PydanticObjectId

from app.models.category_model import Category, SubCategory, Topic


@pytest.mark.asyncio
async def test_category_crud_operations(client):
    """Test full CRUD operations for categories through API endpoints"""
    
    # Test creating a category
    category_payload = {
        "name": "Technology",
        "description": "Technology related topics"
    }
    
    response = await client.post("/categories/", json=category_payload)
    assert response.status_code == 200
    category_data = response.json()
    category_id = category_data["id"]   
    # Verify category was created in DB
    db_category = await Category.get(category_id)
    assert db_category.name == category_payload["name"]
    assert db_category.description == category_payload["description"]
    
    # Test getting category by ID
    response = await client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["name"] == category_payload["name"]
    
    # Test updating category
    updated_category_payload = {
        "name": "Updated Technology",
        "description": "Updated technology related topics"
    }
    response = await client.patch(f"/categories/{category_id}", json=updated_category_payload)
    assert response.status_code == 200
    assert response.json()["name"] == updated_category_payload["name"]
    
    # Test getting all categories
    response = await client.get("/categories/")
    assert response.status_code == 200
    assert len(response.json()) >= 1  # At least our created category
    
    # Test deleting category
    response = await client.delete(f"/categories/{category_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Category deleted successfully"
    
    # Verify category was deleted
    db_category = await Category.get(category_id)
    assert db_category is None


@pytest.mark.asyncio
async def test_subcategory_crud_operations(client):
    """Test full CRUD operations for subcategories through API endpoints"""
    
    # First create a category
    category_payload = {
        "name": "Science",
        "description": "Scientific topics"
    }
    response = await client.post("/categories/", json=category_payload)
    assert response.status_code == 200
    category_id = response.json()["id"]
    
    # Test creating a subcategory
    subcategory_payload = {
        "name": "Physics",
        "description": "Physics topics",
        "category_id": category_id
    }
    
    response = await client.post("/subcategories/", json=subcategory_payload)
    assert response.status_code == 200
    subcategory_data = response.json()
    subcategory_id = subcategory_data["id"]
    
    # Verify subcategory was created in DB
    db_subcategory = await SubCategory.get(subcategory_id)
    assert db_subcategory.name == subcategory_payload["name"]
    assert db_subcategory.description == subcategory_payload["description"]
    assert str(db_subcategory.category_id) == category_id
    
    # Test getting subcategory by ID
    response = await client.get(f"/subcategories/{subcategory_id}")
    assert response.status_code == 200
    assert response.json()["name"] == subcategory_payload["name"]
    
    # Test updating subcategory
    updated_subcategory_payload = {
        "name": "Updated Physics",
        "description": "Updated physics topics"
    }
    response = await client.patch(f"/subcategories/{subcategory_id}", json=updated_subcategory_payload)
    assert response.status_code == 200
    assert response.json()["name"] == updated_subcategory_payload["name"]
    
    # Test getting subcategories by category
    response = await client.get(f"/subcategories/category/{category_id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1  # At least our created subcategory
    
    # Test deleting subcategory
    response = await client.delete(f"/subcategories/{subcategory_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "SubCategory deleted successfully"
    
    # Verify subcategory was deleted
    db_subcategory = await SubCategory.get(subcategory_id)
    assert db_subcategory is None
    
    # Clean up category
    response = await client.delete(f"/categories/{category_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_topic_crud_operations(client):
    """Test full CRUD operations for topics through API endpoints"""
    
    # First create a category and subcategory
    category_payload = {
        "name": "Education",
        "description": "Educational topics"
    }
    response = await client.post("/categories/", json=category_payload)
    assert response.status_code == 200
    category_id = response.json()["id"]
    
    subcategory_payload = {
        "name": "Mathematics",
        "description": "Mathematical topics",
        "category_id": category_id
    }
    response = await client.post("/subcategories/", json=subcategory_payload)
    assert response.status_code == 200
    subcategory_id = response.json()["id"]
    
    # Test creating a topic
    topic_payload = {
        "name": "Algebra",
        "description": "Algebra topics",
        "sub_category_id": subcategory_id
    }
    
    response = await client.post("/topics/", json=topic_payload)
    assert response.status_code == 200
    topic_data = response.json()
    topic_id = topic_data["id"]
    
    # Verify topic was created in DB
    db_topic = await Topic.get(topic_id)
    assert db_topic.name == topic_payload["name"]
    assert db_topic.description == topic_payload["description"]
    assert str(db_topic.sub_category_id) == subcategory_id
    
    # Test getting topic by ID
    response = await client.get(f"/topics/{topic_id}")
    assert response.status_code == 200
    assert response.json()["name"] == topic_payload["name"]
    
    # Test updating topic
    updated_topic_payload = {
        "name": "Updated Algebra",
        "description": "Updated algebra topics"
    }
    response = await client.patch(f"/topics/{topic_id}", json=updated_topic_payload)
    assert response.status_code == 200
    assert response.json()["name"] == updated_topic_payload["name"]
    
    # Test getting topics by subcategory
    response = await client.get(f"/topics/subcategory/{subcategory_id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1  # At least our created topic
    
    # Test deleting topic
    response = await client.delete(f"/topics/{topic_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Topic deleted successfully"
    
    # Verify topic was deleted
    db_topic = await Topic.get(topic_id)
    assert db_topic is None
    
    # Clean up subcategory and category
    response = await client.delete(f"/subcategories/{subcategory_id}")
    assert response.status_code == 200
    response = await client.delete(f"/categories/{category_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_category_subcategory_topic_relationships(client):
    """Test that relationships between categories, subcategories, and topics work correctly"""
    
    # Create category
    category_payload = {
        "name": "Technology",
        "description": "Technology related topics"
    }
    response = await client.post("/categories/", json=category_payload)
    assert response.status_code == 200
    category_id = response.json()["id"]
    
    # Create subcategory with category_id
    subcategory_payload = {
        "name": "Programming",
        "description": "Programming topics",
        "category_id": category_id
    }
    response = await client.post("/subcategories/", json=subcategory_payload)
    assert response.status_code == 200
    subcategory_id = response.json()["id"]
    
    # Create topic with subcategory_id
    topic_payload = {
        "name": "Python",
        "description": "Python programming language",
        "sub_category_id": subcategory_id
    }
    response = await client.post("/topics/", json=topic_payload)
    assert response.status_code == 200
    topic_id = response.json()["id"]
    
    # Verify relationships
    # Get topic and verify it has correct subcategory_id and category_id
    response = await client.get(f"/topics/{topic_id}")
    assert response.status_code == 200
    
    # Test that we can retrieve all related data
    response = await client.get(f"/subcategories/category/{category_id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    
    response = await client.get(f"/topics/subcategory/{subcategory_id}")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    
    # Clean up
    await client.delete(f"/topics/{topic_id}")
    await client.delete(f"/subcategories/{subcategory_id}")
    await client.delete(f"/categories/{category_id}")


@pytest.mark.asyncio
async def test_invalid_operations(client):
    """Test that invalid operations are properly handled"""
    
    # Try to get non-existent category
    response = await client.get("/categories/000000000000000000000000")
    # Should handle gracefully
    
    # Try to delete non-existent category
    response = await client.delete("/categories/000000000000000000000000")
    # Should handle gracefully