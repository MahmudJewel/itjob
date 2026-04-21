from uuid import uuid4

import pytest

from app.models.user_model import User


@pytest.mark.asyncio
async def test_create_user_creates_db_object(client):
    email = f"itjob_user_{uuid4().hex[:8]}@mail.com"
    payload = {
        "email": email,
        "password": "MyStrongPass123!",
        "first_name": "Mahmud",
        "last_name": "Jewel",
        "mobile_number": "01700000000",
    }

    response = await client.post("/users/", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "New user created"
    assert body["data"]["email"] == payload["email"]
    assert body["data"]["mobile_number"] == payload["mobile_number"]
    assert "password" not in body["data"]

    inserted_user = await User.find_one(User.email == payload["email"])
    assert inserted_user is not None
    assert inserted_user.first_name == payload["first_name"]
    assert inserted_user.last_name == payload["last_name"]
    assert inserted_user.mobile_number == payload["mobile_number"]


@pytest.mark.asyncio
async def test_create_user_duplicate_email_returns_400_and_single_object(client):
    email = f"itjob_dup_{uuid4().hex[:8]}@mail.com"
    payload = {
        "email": email,
        "password": "MyStrongPass123!",
        "first_name": "Mahmud",
        "last_name": "Jewel",
        "mobile_number": "01800000000",
    }

    first_response = await client.post("/users/", json=payload)
    second_response = await client.post("/users/", json=payload)

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json() == {"detail": "User already exists"}
    assert await User.find(User.email == payload["email"]).count() == 1
