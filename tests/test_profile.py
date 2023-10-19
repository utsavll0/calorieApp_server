import pytest
from unittest.mock import patch
from application import app
import mongomock


@pytest.fixture
def client():
    with mongomock.patch():
        with app.test_client() as client:
            yield client


def test_get_user_profile(client):
    db = mongomock.MongoClient().db
    
    db.items.insert_one(
        {"email":"ojaskulkarni100@gmail.com" ,"weight":90, "height":180, "target_weight":80,"goal":"75"},
    )
    response = client.get("/user_profile")
    assert response.status_code == 302

