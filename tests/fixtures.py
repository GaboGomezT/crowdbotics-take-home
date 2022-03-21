import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from config import get_session
from main import app as fastapi_app
from models.db import TokenData
from v1.auth_utils import get_token


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="token")
def token_fixture():
    token = TokenData(username="test_name")
    yield token


@pytest.fixture(name="client")
def client_fixture(session: Session, token: TokenData):
    def get_session_override():
        return session

    def get_token_override():
        return token

    fastapi_app.dependency_overrides[get_session] = get_session_override
    fastapi_app.dependency_overrides[get_token] = get_token_override

    client = TestClient(fastapi_app)
    yield client
    fastapi_app.dependency_overrides.clear()
