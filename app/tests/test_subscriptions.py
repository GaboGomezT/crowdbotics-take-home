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
        app.save(session)
        sub = Subscription(user_id=user.id, app_id=app.id, plan_id=basic_plan.id)
        sub.save(session)
    response = client.get("/api/v1/subscriptions/")
    fastapi_app.dependency_overrides.clear()
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 6
