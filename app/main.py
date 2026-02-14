from fastapi import FastAPI
from app.users.routes import user_router
version = "v1"
app = FastAPI(
    title="User Management",
    description="A REST API for User Management web service",
    version=version

)

app.include_router(user_router, prefix=f"/api/{version}")