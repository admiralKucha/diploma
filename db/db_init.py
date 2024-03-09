from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/diploma", pool_size=5,
                             isolation_level="READ COMMITTED")

sync_engine = create_engine("postgresql://postgres:postgres@localhost/diploma")

Session = async_sessionmaker(engine, autoflush=False, autocommit=False)





