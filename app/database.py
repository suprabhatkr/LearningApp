import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Database")

# Setup async engines
# We default to Postgres, and fallback to SQLite if it fails
DB_URL = settings.get_postgres_url
USE_POSTGRES = False

def is_postgres_active() -> bool:
    return USE_POSTGRES

# Create the Engine
connect_args = {}
if DB_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_async_engine(
    DB_URL,
    echo=False,
    connect_args=connect_args
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Declarative base for ORM Models
class Base(DeclarativeBase):
    pass

# Dependency to yield database sessions to endpoints
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Helper function to initialize database tables
async def init_db():
    global engine, async_session_maker
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        # If postgres fails, let's fall back to local sqlite engine
        logger.info("Falling back to SQLite database...")
        engine = create_async_engine(
            "sqlite+aiosqlite:///./ascend_learning_fallback.db",
            connect_args={"check_same_thread": False}
        )
        async_session_maker = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Fallback SQLite database initialized successfully.")
