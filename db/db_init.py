from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/diploma", pool_size=5,
                             isolation_level="READ COMMITTED")
Session = async_sessionmaker(engine, autoflush=False, autocommit=False)





