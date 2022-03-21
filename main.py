from fastapi import Depends, FastAPI
from sqlmodel import Session
from sqlmodel import SQLModel

from config import engine, get_session
from models.plans import Plan
from v1 import apps, auth, plans, subscriptions


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI(
    title="Hiring Example API",
    description="API documentation for Hiring Example App",
    version="v1",
    servers=[{"url": ""}],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    session = Session(engine)
    Plan.setup(session=session)
    session.close()


app.include_router(apps.router)
app.include_router(plans.router)
app.include_router(subscriptions.router)
app.include_router(auth.router)
