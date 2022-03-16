from fastapi import FastAPI

from app.v1 import apps, auth, plans, subscriptions

app = FastAPI(
    title="Hiring Example API",
    description="API documentation for Hiring Example App",
    version="v1",
    servers=[{"url": ""}],
)

app.include_router(apps.router)
app.include_router(plans.router)
app.include_router(subscriptions.router)
app.include_router(auth.router)
