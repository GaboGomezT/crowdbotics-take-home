from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.main import app as fastapi_app
from app.config import get_session
from sqlmodel.pool import StaticPool
import pytest

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")   
def client_fixture(session: Session):   
    def get_session_override():   
        return session

    fastapi_app.dependency_overrides[get_session] = get_session_override   

    client = TestClient(fastapi_app)   
    yield client   
    fastapi_app.dependency_overrides.clear()

def test_create_app(client: TestClient):
        response = client.post(
        "/api/v1/apps/", json={
                "name": "Crowdbotics", 
                "description": "No-code app builder",
                "type": "Web",
                "framework": "Django",
                "domain_name": "crowdbotics.com"
                }
        )
        fastapi_app.dependency_overrides.clear()
        data = response.json()
        print(data)
        assert response.status_code == 200  
        assert data["name"] == "Crowdbotics"  
        assert data["description"] == "No-code app builder"  
        assert data["type"] == "Web" 
        assert data["framework"] == "Django" 
        assert data["domain_name"] == "crowdbotics.com" 
        assert type(data["id"]) is int

# Code below omitted 👇
