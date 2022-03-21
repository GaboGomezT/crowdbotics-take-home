from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app as fastapi_app
from app.models.db import App, Subscription, User
from app.models.plans import Plan
from app.tests.fixtures import client_fixture, session_fixture, token_fixture


def test_api_v1_subscriptions_list(session: Session, client: TestClient):
    user = User(username="test_name", hashed_password="pass")
    user.save(session)
    Plan.setup(session)
    basic_plan = Plan.find(1, session)
    for _ in range(6):
        app = App(
            name="Crowdbotics",
            description="No-code app builder",
            type="Web",
            framework="Django",
            user=user,
        )
        sub = Subscription(user_id=user.id, app_id=app.id, plan_id=basic_plan.id)
        sub.save(session)
    response = client.get("/api/v1/subscriptions/")
    fastapi_app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 6


def test_api_v1_subscriptions_create(session: Session, client: TestClient):
    user = User(username="test_name", hashed_password="pass")
    user.save(session)
    Plan.setup(session)
    app = App(
        name="Crowdbotics",
        description="No-code app builder",
        type="Web",
        framework="Django",
        user=user,
    )
    app.save(session)
    response = client.post(
        "/api/v1/subscriptions/",
        json={
            "plan_id": 1,
            "app_id": app.id,
            "active": True,
        },
    )

    fastapi_app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert data["plan_id"] == 1
    assert data["app_id"] == app.id
    assert data["active"] == True
    assert data["user_id"] == user.id


def test_api_v1_subscriptions_read(session: Session, client: TestClient):
    user = User(username="test_name", hashed_password="pass")
    user.save(session)
    Plan.setup(session)

    app = App(
        name="Crowdbotics",
        description="No-code app builder",
        type="Web",
        framework="Django",
        user=user,
    )
    sub = Subscription(user_id=user.id, app_id=app.id, plan_id=2)
    sub.save(session)
    response = client.get(f"/api/v1/subscriptions/{sub.id}/")
    data = response.json()

    assert response.status_code == 200

    sub_dict = sub.dict()
    sub_dict["created_at"] = sub_dict["created_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
    sub_dict["updated_at"] = sub_dict["updated_at"].strftime("%Y-%m-%dT%H:%M:%S.%f")
    assert data == sub_dict


def test_api_v1_subscriptions_update(session: Session, client: TestClient):
    user = User(username="test_name", hashed_password="pass")
    user.save(session)
    Plan.setup(session)

    app = App(
        name="Crowdbotics",
        description="No-code app builder",
        type="Web",
        framework="Django",
        user=user,
    )
    sub = Subscription(user_id=user.id, app_id=app.id, plan_id=2)
    sub.save(session)

    new_data = {
        "active": True,
        "app_id": app.id,
        "plan_id": 3,
    }
    response = client.put(
        f"/api/v1/subscriptions/{sub.id}/",
        json=new_data,
    )
    data = response.json()

    assert response.status_code == 200

    for key, value in new_data.items():
        assert data[key] == value


def test_api_v1_subscriptions_partial_update(session: Session, client: TestClient):
    user = User(username="test_name", hashed_password="pass")
    user.save(session)
    Plan.setup(session)

    app = App(
        name="Crowdbotics",
        description="No-code app builder",
        type="Web",
        framework="Django",
        user=user,
    )
    sub = Subscription(user_id=user.id, app_id=app.id, plan_id=2)
    sub.save(session)

    new_data = {"active": False}
    response = client.patch(
        f"/api/v1/subscriptions/{sub.id}/",
        json=new_data,
    )
    data = response.json()

    assert response.status_code == 200

    assert data["active"] == False
    assert data["app_id"] == app.id
    assert data["plan_id"] == 2
