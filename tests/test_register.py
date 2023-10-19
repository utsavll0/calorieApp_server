import pytest
from unittest.mock import patch
from application import app
import mongomock


@pytest.fixture
def client():
    with mongomock.patch():
        with app.test_client() as client:
            yield client


def test_get_user(client):
    db = mongomock.MongoClient().db
    db.items.insert_one(
        {
            "name": "OjasTest",
            "pwd": "hshaksjn",
            "weight": 90,
            "height": 180,
            "target_weight": 80,
            "start_date": "2023-10-15",
            "target_date": "2023-11-15"
        }, )
    response = client.get("/register")
    assert response.status_code == 200


def test_insert_user(client):
    # Make a POST request to the /items endpoint with a JSON payload
    response = client.post("/register",
                           json={
                               "name": "OjasTest",
                               "pwd": "hshaksjn",
                               "weight": "90",
                               "height": "180",
                               "target_weight": "80",
                               "start_date": "2023-10-15",
                               "target_date": "2023-11-15"
                           })
    # Assert the response status code is 201 Created
    assert response.status_code == 200
