from db import db
from fastapi import FastAPI
from config import config
import uvicorn


def init_app():
    db.init(config.DB_CONFIG)

    app = FastAPI(
        title="Users App",
        description="Handling Our User",
        version="1",
    )

    from views import api

    app.include_router(
        api,
        prefix="/api/v1",
    )

    return app


app = init_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
