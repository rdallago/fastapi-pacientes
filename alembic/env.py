
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Importamos la configuración de nuestra base de datos
from database import Base, DATABASE_URL
from entidades.paciente import Paciente
from entidades.observacion import Observacion

# Configuración de Alembic
config = context.config

# Configuración de logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Modelos SQLAlchemy registrados en Base
# Cuando creemos la entidad Paciente, la importaremos aquí.

# Metadatos para detectar cambios en las entidades
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Ejecuta migraciones sin conexión directa a la BD.
    """
    url = DATABASE_URL.render_as_string(
        hide_password=False
    )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Ejecuta migraciones conectándose a PostgreSQL.
    """

    # Tomamos la configuración de alembic.ini
    configuration = config.get_section(
        config.config_ini_section,
        {}
    )

    # Utilizamos la conexión definida en database.py
    configuration["sqlalchemy.url"] = (
        DATABASE_URL.render_as_string(
            hide_password=False
        )
    )

    # Creamos el motor de conexión
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Ejecutamos las migraciones
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# Determinamos el modo de ejecución
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
