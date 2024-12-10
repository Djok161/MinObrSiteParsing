from contextlib import asynccontextmanager, contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Session

from .config import *

engine_async = create_async_engine(get_db_url_async())
engine_sync = create_engine(get_db_url_sync())


class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def get_session_async() -> AsyncSession:
    async with AsyncSession(engine_async) as conn:
        yield conn


@contextmanager
def get_session_sync() -> Session:
    session = Session(engine_sync)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
