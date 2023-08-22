from db import db
from fastapi import FastAPI
from config import config
import uvicorn
import logging


logger = logging.getLogger(__name__)


def init_app():
    app = FastAPI(
        title="Users App",
        description="Handling Our User",
        version="1",
    )

    @app.on_event("startup")
    def startup():
        db.connect(config.DB_CONFIG)

    @app.on_event("shutdown")
    async def shutdown():
        await db.disconnect()

    from views import api

    app.include_router(
        api,
        prefix="/api/v1",
    )

    return app


app = init_app()
