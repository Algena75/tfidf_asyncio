from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (Mapped, declarative_base, declared_attr,
                            mapped_column, sessionmaker)

from app.core.config import settings


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return f'{cls.__name__.lower()}s'

    # id: Mapped[int] = mapped_column(primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.DATABASE_URL)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
