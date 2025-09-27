from typing import Any

from alembic import context
from sqlalchemy import create_engine, pool

from ninsho.config import config
from ninsho.db.base import metadata
from ninsho.db.register_models import setup_models

# Force the use of a non-async engine, as Alembic doesn't support async versions
db_dsn = config.database_url
if db_dsn.startswith("postgresql+asyncpg://"):
    db_dsn = db_dsn.replace("postgresql+asyncpg://", "postgresql://", 1)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an Engine is acceptable here as well. By
    skipping the Engine creation we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    context.configure(
        url=db_dsn,
        target_metadata=metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection with the context.
    """
    connectable = create_engine(db_dsn, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=metadata)
        with context.begin_transaction():
            context.run_migrations()


# models imported before schema creation or migrations.
setup_models()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
