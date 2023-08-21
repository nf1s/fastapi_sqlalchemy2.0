from db import db
from fastapi import FastAPI
from config import config


def init_app():
    db.init(config.DB_CONFIG)

    app = FastAPI(
        title="Users App",
        description="Handling Our User",
        version="1",
    )

    @app.on_event("startup")
    async def startup():
        await db.create_all()

    from views import api

    app.include_router(
        api,
        prefix="/api/v1",
    )

    return app


app = init_app()
