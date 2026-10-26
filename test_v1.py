import pytest
from v1 import app, reviews


@pytest.fixture
def client():
    app.config["TESTING"] = True
    reviews.clear()

    with app.test_client() as test_client:
        yield test_client

    reviews.clear()


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 302


def test_reviews_page(client):
    response = client.get("/reviews")

    assert response.status_code == 200
    assert b"Review System - V1" in response.data


def test_add_review_successfully(client):
    response = client.post(
        "/add_review",
        data={
            "product": "Laptop",
            "rating": "5",
            "comment": "Excellent product"
        }
    )

    assert response.status_code == 302
    assert len(reviews) == 1
    assert reviews[0]["product"] == "Laptop"
    assert reviews[0]["rating"] == 5
    assert reviews[0]["comment"] == "Excellent product"


def test_reject_rating_below_one(client):
    response = client.post(
        "/add_review",
        data={
            "product": "Laptop",
            "rating": "0",
            "comment": "Poor product"
        }
    )

    assert response.status_code == 400
    assert len(reviews) == 0


def test_reject_rating_above_five(client):
    response = client.post(
        "/add_review",
        data={
            "product": "Laptop",
            "rating": "6",
            "comment": "Poor product"
        }
    )

    assert response.status_code == 400
    assert len(reviews) == 0


def test_reject_missing_product(client):
    response = client.post(
        "/add_review",
        data={
            "product": "",
            "rating": "4",
            "comment": "Good product"
        }
    )

    assert response.status_code == 400
    assert len(reviews) == 0


def test_reject_missing_comment(client):
    response = client.post(
        "/add_review",
        data={
            "product": "Laptop",
            "rating": "4",
            "comment": ""
        }
    )

    assert response.status_code == 400
    assert len(reviews) == 0


def test_submitted_review_appears_on_page(client):
    client.post(
        "/add_review",
        data={
            "product": "Phone",
            "rating": "4",
            "comment": "Good quality"
        }
    )

    response = client.get("/reviews")

    assert response.status_code == 200
    assert b"Phone" in response.data
    assert b"Good quality" in response.data


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["version"] == "v1"
