from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Load models for Alembic
from db.models import Base
target_metadata = Base.metadata


# This is the function that Alembic calls to get the metadata about your database
def run_migrations_offline():
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    configuration = context.config
    engine = engine_from_config(
        configuration.get_section(configuration.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()


# If we're offline, skip the rest of this and just run the migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
