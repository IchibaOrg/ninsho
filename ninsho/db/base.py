from sqlalchemy import MetaData
from sqlalchemy.orm import registry, DeclarativeBase, MappedAsDataclass
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from ninsho.config import config


DB_COMMAND_TIMEOUT_SECONDS = 5 * 60

print("Creating db engine")
engine = create_async_engine(
    config.database_url,
    future=True,
    poolclass=NullPool, # disables the connection pooling for now
    connect_args={"command_timeout": DB_COMMAND_TIMEOUT_SECONDS},  # sets how long a query can run before being killed.
)

metadata = MetaData()
mapper_registry = registry(metadata=metadata)


def get_db_session(autoflush: bool = True) -> AsyncSession:
    return AsyncSession(bind=engine, future=True, expire_on_commit=False, autoflush=autoflush)


class BaseModel(MappedAsDataclass, DeclarativeBase, repr=False, kw_only=True):  # type: ignore
    registry = mapper_registry
    metadata = mapper_registry.metadata

