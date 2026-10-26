import pytest
import v3


@pytest.fixture(autouse=True)
def reset_reviews():
    """Reset sample data before each test."""
    v3.reviews[:] = [
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
        },
        {
            "id": 3,
            "name": "Priya",
            "rating": 3,
            "comment": "Average experience."
        }
    ]


@pytest.fixture
def client():
    v3.app.config["TESTING"] = True

    with v3.app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Delete Review" in response.data


def test_reviews_are_displayed(client):
    response = client.get("/")
    assert b"Mokshitha" in response.data
    assert b"Rahul" in response.data
    assert b"Priya" in response.data


def test_delete_review_successfully(client):
    response = client.post("/delete_review/1")

    assert response.status_code == 302
    assert len(v3.reviews) == 2
    assert all(review["id"] != 1 for review in v3.reviews)


def test_delete_another_review(client):
    response = client.post("/delete_review/2")

    assert response.status_code == 302
    assert all(review["id"] != 2 for review in v3.reviews)


def test_nonexistent_review(client):
    response = client.post("/delete_review/999")

    assert response.status_code == 404
    assert len(v3.reviews) == 3


def test_remaining_reviews_are_displayed(client):
    client.post("/delete_review/1")

    response = client.get("/")

    assert response.status_code == 200
    assert b"Rahul" in response.data
    assert b"Priya" in response.data
    assert b"Mokshitha" not in response.data


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["version"] == "v3"