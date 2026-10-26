import pytest
import v2


@pytest.fixture(autouse=True)
def reset_reviews():
    """Reset sample data before each test."""
    v2.reviews[:] = [
        {
            "id": 1,
            "name": "Mokshitha",
            "rating": 5,
            "comment": "Excellent service!"
        },
        {
            "id": 2,
            "name": "Rahul",
            "rating": 4,
            "comment": "Good experience."
        }
    ]


@pytest.fixture
def client():
    v2.app.config["TESTING"] = True

    with v2.app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Edit Review" in response.data


def test_reviews_are_displayed(client):
    response = client.get("/")
    assert b"Mokshitha" in response.data
    assert b"Rahul" in response.data


def test_edit_review_successfully(client):
    response = client.post(
        "/edit_review/1",
        data={
            "name": "Mokshitha",
            "rating": "3",
            "comment": "Updated review"
        }
    )

    assert response.status_code == 302
    assert v2.reviews[0]["rating"] == 3
    assert v2.reviews[0]["comment"] == "Updated review"


def test_edit_review_name(client):
    client.post(
        "/edit_review/1",
        data={
            "name": "New Name",
            "rating": "5",
            "comment": "Great"
        }
    )

    assert v2.reviews[0]["name"] == "New Name"


def test_invalid_rating_too_high(client):
    response = client.post(
        "/edit_review/1",
        data={
            "name": "Mokshitha",
            "rating": "6",
            "comment": "Updated"
        }
    )

    assert response.status_code == 400


def test_invalid_rating_too_low(client):
    response = client.post(
        "/edit_review/1",
        data={
            "name": "Mokshitha",
            "rating": "0",
            "comment": "Updated"
        }
    )

    assert response.status_code == 400


def test_missing_comment(client):
    response = client.post(
        "/edit_review/1",
        data={
            "name": "Mokshitha",
            "rating": "4",
            "comment": ""
        }
    )

    assert response.status_code == 400


def test_nonexistent_review(client):
    response = client.post(
        "/edit_review/999",
        data={
            "name": "Test",
            "rating": "4",
            "comment": "Test comment"
        }
    )

    assert response.status_code == 404


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["version"] == "v2"