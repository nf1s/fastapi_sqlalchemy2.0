import logging
from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config import config

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    def __init__(self):
        self.session = None
        self.engine = None

    def __getattr__(self, name):
        return getattr(self.session, name)

    def init(self, db_config):
        self.engine = create_async_engine(
            config.DB_CONFIG,
            pool_pre_ping=True,
            echo=True,
        )

        self.session = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            future=True,
        )

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db = Database()


async def get_db():
    session = db.session()
    try:
        yield session
    except SQLAlchemyError as e:
        logger.exception(e)
        await session.rollback()
