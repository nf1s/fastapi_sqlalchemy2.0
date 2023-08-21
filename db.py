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
        self.__session = None
        self.__engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self, db_config):
        self.__engine = create_async_engine(
            config.DB_CONFIG,
            pool_pre_ping=True,
            echo=True,
        )

        self.__session = async_sessionmaker(
            bind=self.__engine,
            autoflush=False,
            future=True,
        )

    def create_all(self):
        Base.metadata.create_all(self.__engine)

    def drop_all(self):
        Base.metadata.drop_all(self.__engine)

    async def get_session(self) -> AsyncIterator[async_sessionmaker]:
        session = self._session()
        try:
            yield session
        except SQLAlchemyError as e:
            logger.exception(e)
            await session.rollback()
        finally:
            await session.close()


db = Database()
