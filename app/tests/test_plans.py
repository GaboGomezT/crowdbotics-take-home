from typing import List

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.db import User
from app.models.plans import Plan
from app.tests.fixtures import session_fixture  # noqa: E731
from app.tests.fixtures import client_fixture, token_fixture  # noqa: E731


def test_api_v1_plans_list(session: Session, client: TestClient):
    user = User(username="test_name", hashed_password="pass")
    user.save(session)

    Plan.setup(session)

    response = client.get(f"/api/v1/plans/")
    data: List[Plan] = response.json()

    assert response.status_code == 200

    assert len(data) == 3

    assert data[0]["name"] == "Free"
    assert data[0]["description"] == "Free Plan"
    assert data[0]["price"] == 0

    assert data[1]["name"] == "Standard"
    assert data[1]["description"] == "Standard Plan"
    assert data[1]["price"] == 10

    assert data[2]["name"] == "Pro"
    assert data[2]["description"] == "Pro Plan"
    assert data[2]["price"] == 25


def test_api_v1_plans_read(session: Session, client: TestClient):
    user = User(username="test_name", hashed_password="pass")
    user.save(session)

    Plan.setup(session)

    response = client.get(f"/api/v1/plans/1/")
    data = response.json()

    assert response.status_code == 200

    assert data["name"] == "Free"
    assert data["description"] == "Free Plan"
    assert data["price"] == 0
