from fastapi import FastAPI
from sqlmodel import SQLModel

from app.models.db import engine
from app.v1 import apps, auth, plans, subscriptions


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


app.include_router(apps.router)
app.include_router(plans.router)
app.include_router(subscriptions.router)
app.include_router(auth.router)
