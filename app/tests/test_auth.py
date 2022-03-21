
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.db import User
from app.tests.fixtures import client_fixture, session_fixture, token_fixture # noqa: E731


def test_login_for_access_token(session: Session, client: TestClient):
    user = User(username="test_name")
    user.set_hashed_password("pass")
    user.save_new(session)

    response = client.post(f"/token", data={
        "username": "test_name",
        "password": "pass"
    })
    data = response.json()

    assert response.status_code == 200

    assert type(data["access_token"]) is str
    assert data["token_type"] == "bearer"

def test_register(client: TestClient):
    response = client.post(f"/register", data={
        "username": "test_name",
        "password": "pass"
    })
    data = response.json()

    assert response.status_code == 200

    assert type(data["access_token"]) is str
    assert data["token_type"] == "bearer"

def test_change_password(session: Session, client: TestClient):
    user = User(username="test_name")
    user.set_hashed_password("pass")
    user.save_new(session)

    response = client.post(f"/change-password", json={
        "username": "test_name",
        "old_password": "pass",
        "new_password": "new_pass"
    })

    assert response.status_code == 200

    assert user.verify_password("new_pass")