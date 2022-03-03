from fastapi import FastAPI

from app.api.api_v1.routes import api_router
from app.config import settings


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        openapi_url="/openapi.json",
    )
    application.include_router(api_router)

    return application


app = create_application()
