from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app as fastapi_app
from app.models.db import App, User
from app.tests.fixtures import session_fixture  # noqa: E731
from app.tests.fixtures import client_fixture, token_fixture  # noqa: E731


def test_api_v1_apps_create(session: Session, client: TestClient):
    user = User(username="test_name", hashed_password="pass")
    user.save(session)

    response = client.post(
        "/api/v1/apps/",
        json={
            "name": "Crowdbotics",
            "description": "No-code app builder",
            "type": "Web",
            "framework": "Django",
            "domain_name": "crowdbotics.com",
        },
    )
    fastapi_app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Crowdbotics"
    assert data["description"] == "No-code app builder"
    assert data["type"] == "Web"
    assert data["framework"] == "Django"
    assert data["domain_name"] == "crowdbotics.com"
    assert type(data["id"]) is int


def test_api_v1_apps_read(session: Session, client: TestClient):
    app = App(
        name="Crowdbotics",
        description="No-code app builder",
        type="Web",
        framework="Django",
        user=User(username="test_name", hashed_password="pass"),
    )
    app.save(session)

    response = client.get(f"/api/v1/apps/{app.id}/")
    data = response.json()

    assert response.status_code == 200

    app_dict = app.dict()
    app_dict["created_at"] = app_dict["created_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
    app_dict["updated_at"] = app_dict["updated_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert data == app_dict


def test_api_v1_apps_list(session: Session, client: TestClient):
    user = User(username="test_name", hashed_password="pass")
    first_app = App(
        name="Crowdbotics",
        description="No-code app builder",
        type="Web",
        framework="Django",
        user=user,
    )
    first_app.save(session)
    second_app = App(
        name="Some other app",
        description="No-code app builder",
        type="Web",
        framework="Django",
        user=user,
    )
    second_app.save(session)
    apps = [first_app, second_app]

    response = client.get(f"/api/v1/apps/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2

    for index, app in enumerate(apps):
        app_dict = app.dict()
        app_dict["created_at"] = app_dict["created_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
        app_dict["updated_at"] = app_dict["updated_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
        assert data[index] == app_dict


def test_api_v1_apps_update(session: Session, client: TestClient):
    app = App(
        name="Crowdbotics",
        description="No-code app builder",
        type="Web",
        framework="Django",
        user=User(username="test_name", hashed_password="pass"),
    )
    app.save(session)

    new_data = {
        "name": "Crowdbotics 2.0",
        "description": "No-code app builder",
        "type": "Web",
        "framework": "Django",
        "domain_name": "crowdbotics.io",
    }
    response = client.put(
        f"/api/v1/apps/{app.id}/",
        json=new_data,
    )
    data = response.json()

    assert response.status_code == 200

    for key, value in new_data.items():
        assert data[key] == value


def test_api_v1_apps_partial_update(session: Session, client: TestClient):
    app = App(
        name="Crowdbotics",
        description="No-code app builder",
        type="Web",
        framework="Django",
        user=User(username="test_name", hashed_password="pass"),
    )
    app.save(session)

    new_data = {"name": "Crowdbotics 2.0"}
    response = client.patch(
        f"/api/v1/apps/{app.id}/",
        json=new_data,
    )
    data = response.json()
    assert response.status_code == 200

    assert data["name"] == "Crowdbotics 2.0"
    assert data["description"] == "No-code app builder"
    assert data["type"] == "Web"
    assert data["framework"] == "Django"


def test_api_v1_apps_delete(session: Session, client: TestClient):
    app = App(
        name="Crowdbotics",
        description="No-code app builder",
        type="Web",
        framework="Django",
        user=User(username="test_name", hashed_password="pass"),
    )
    app.save(session)

    response = client.delete(f"/api/v1/apps/{app.id}/")

    assert response.status_code == 204

    all_apps = App.get_all(session)
    assert len(all_apps) == 0
